"""
Tests unitaires pour le gestionnaire de sessions
"""
import unittest
from datetime import datetime, timedelta
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.session import UserSession, SessionManager


class TestUserSession(unittest.TestCase):
    """Tests pour la classe UserSession"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.user_id = 123456789
        self.session = UserSession(self.user_id)

    def test_init(self):
        """Test de l'initialisation d'une session"""
        self.assertEqual(self.session.user_id, self.user_id)
        self.assertIsNone(self.session.current_mode)
        self.assertEqual(len(self.session.conversation_history), 0)
        self.assertIsInstance(self.session.started_at, datetime)
        self.assertIsInstance(self.session.last_activity, datetime)

    def test_add_message(self):
        """Test de l'ajout de messages à l'historique"""
        self.session.add_message("user", "Bonjour")
        self.assertEqual(len(self.session.conversation_history), 1)
        self.assertEqual(self.session.conversation_history[0]["role"], "user")
        self.assertEqual(self.session.conversation_history[0]["content"], "Bonjour")

        self.session.add_message("assistant", "Salut")
        self.assertEqual(len(self.session.conversation_history), 2)

    def test_message_history_limit(self):
        """Test de la limitation de l'historique"""
        # Définir une limite basse pour les tests
        os.environ['MAX_CONVERSATION_HISTORY'] = '5'

        # Ajouter plus de messages que la limite
        for i in range(10):
            self.session.add_message("user", f"Message {i}")

        # Vérifier que l'historique est limité
        self.assertLessEqual(len(self.session.conversation_history), 5)

        # Nettoyer
        del os.environ['MAX_CONVERSATION_HISTORY']

    def test_reset(self):
        """Test de la réinitialisation de session"""
        self.session.add_message("user", "Test")
        self.session.reset()

        self.assertIsNone(self.session.current_mode)
        self.assertEqual(len(self.session.conversation_history), 0)

    def test_is_expired(self):
        """Test de la vérification d'expiration"""
        # Session récente ne doit pas être expirée
        self.assertFalse(self.session.is_expired())

        # Simuler une session expirée en modifiant last_activity
        os.environ['SESSION_TIMEOUT_MINUTES'] = '1'
        self.session.last_activity = datetime.now() - timedelta(minutes=2)
        self.assertTrue(self.session.is_expired())

        # Nettoyer
        del os.environ['SESSION_TIMEOUT_MINUTES']

    def test_get_history(self):
        """Test de la récupération de l'historique"""
        self.session.add_message("user", "Message 1")
        self.session.add_message("assistant", "Réponse 1")

        history = self.session.get_history()
        self.assertEqual(len(history), 2)
        # Vérifier que c'est une copie
        self.assertIsNot(history, self.session.conversation_history)

    def test_rate_limit(self):
        """Test du rate limiting"""
        os.environ['MAX_MESSAGES_PER_MINUTE'] = '3'

        # Les 3 premiers messages doivent passer
        self.assertTrue(self.session.check_rate_limit())
        self.assertTrue(self.session.check_rate_limit())
        self.assertTrue(self.session.check_rate_limit())

        # Le 4ème devrait échouer
        self.assertFalse(self.session.check_rate_limit())

        # Nettoyer
        del os.environ['MAX_MESSAGES_PER_MINUTE']

    def test_validate_message_length(self):
        """Test de la validation de la longueur des messages"""
        # Message valide
        is_valid, error = self.session.validate_message_length("Message normal")
        self.assertTrue(is_valid)
        self.assertIsNone(error)

        # Message vide
        is_valid, error = self.session.validate_message_length("   ")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        # Message trop long
        os.environ['MAX_MESSAGE_LENGTH'] = '10'
        is_valid, error = self.session.validate_message_length("Message beaucoup trop long")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

        # Nettoyer
        del os.environ['MAX_MESSAGE_LENGTH']


class TestSessionManager(unittest.TestCase):
    """Tests pour la classe SessionManager"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.manager = SessionManager()

    def test_get_session(self):
        """Test de la récupération d'une session"""
        user_id = 123456789
        session = self.manager.get_session(user_id)

        self.assertIsInstance(session, UserSession)
        self.assertEqual(session.user_id, user_id)

        # Vérifier que la même session est retournée
        session2 = self.manager.get_session(user_id)
        self.assertIs(session, session2)

    def test_reset_session(self):
        """Test de la réinitialisation d'une session"""
        user_id = 123456789
        session = self.manager.get_session(user_id)
        session.add_message("user", "Test")

        self.manager.reset_session(user_id)

        # Vérifier que la session a été réinitialisée
        self.assertEqual(len(session.conversation_history), 0)

    def test_reset_nonexistent_session(self):
        """Test de reset d'une session qui n'existe pas"""
        # Ne devrait pas lever d'erreur
        self.manager.reset_session(999999999)

    def test_cleanup_expired_sessions(self):
        """Test du nettoyage des sessions expirées"""
        os.environ['SESSION_TIMEOUT_MINUTES'] = '1'

        # Créer une session récente
        user_id_1 = 111
        session_1 = self.manager.get_session(user_id_1)

        # Créer une session expirée
        user_id_2 = 222
        session_2 = self.manager.get_session(user_id_2)
        session_2.last_activity = datetime.now() - timedelta(minutes=2)

        # Nettoyer
        self.manager.cleanup_expired_sessions()

        # Vérifier que seule la session récente reste
        self.assertIn(user_id_1, self.manager.sessions)
        self.assertNotIn(user_id_2, self.manager.sessions)

        # Nettoyer
        del os.environ['SESSION_TIMEOUT_MINUTES']

    def test_get_active_sessions_count(self):
        """Test du comptage des sessions actives"""
        os.environ['SESSION_TIMEOUT_MINUTES'] = '1'

        # Créer 2 sessions récentes
        self.manager.get_session(111)
        self.manager.get_session(222)

        # Créer 1 session expirée
        session_3 = self.manager.get_session(333)
        session_3.last_activity = datetime.now() - timedelta(minutes=2)

        # Vérifier le comptage
        self.assertEqual(self.manager.get_active_sessions_count(), 2)

        # Nettoyer
        del os.environ['SESSION_TIMEOUT_MINUTES']


if __name__ == '__main__':
    unittest.main()
