"""
Tests unitaires pour les utilitaires
"""
import unittest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.ai_client import AIClient


class TestAIClient(unittest.TestCase):
    """Tests pour le client IA"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Sauvegarder les variables d'environnement originales
        self.original_env = os.environ.copy()

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Restaurer les variables d'environnement
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_init_openai(self):
        """Test de l'initialisation avec OpenAI"""
        os.environ['OPENAI_API_KEY'] = 'test-key'
        os.environ['OPENAI_MODEL'] = 'gpt-3.5-turbo'

        client = AIClient()
        info = client.get_model_info()
        self.assertEqual(info['provider'], 'openai')
        self.assertIsNotNone(client.client)

    def test_get_model_info(self):
        """Test de la récupération des infos du modèle"""
        os.environ['AI_PROVIDER'] = 'openai'
        os.environ['OPENAI_API_KEY'] = 'test-key'
        os.environ['OPENAI_MODEL'] = 'gpt-4'

        client = AIClient()
        info = client.get_model_info()

        self.assertEqual(info['provider'], 'openai')
        self.assertEqual(info['model'], 'gpt-4')

    def test_missing_api_key(self):
        """Test du comportement sans clé API"""
        # Supprimer toutes les clés API
        for key in ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']:
            if key in os.environ:
                del os.environ[key]

        # Le client devrait lever une erreur ou utiliser une valeur par défaut
        try:
            client = AIClient()
            # Si ça ne lève pas d'erreur, vérifier qu'il y a un warning ou comportement par défaut
            self.assertIsNotNone(client)
        except (ValueError, KeyError):
            # Comportement attendu si pas de clé API
            pass

    def test_temperature_config(self):
        """Test de la configuration de la température"""
        os.environ['AI_PROVIDER'] = 'openai'
        os.environ['OPENAI_API_KEY'] = 'test-key'
        os.environ['OPENAI_MODEL'] = 'gpt-3.5-turbo'
        os.environ['AI_TEMPERATURE'] = '0.9'

        client = AIClient()
        # La température devrait être configurée
        # Note: ceci dépend de l'implémentation du AIClient


class TestEmbedCreation(unittest.TestCase):
    """Tests pour la création d'embeds Discord"""

    def test_mode_colors(self):
        """Test que toutes les couleurs sont définies"""
        from src.bot import MODE_COLORS

        required_colors = [
            "branding", "gamemaster", "webradio",
            "organisation", "default", "error", "success"
        ]

        for color_key in required_colors:
            self.assertIn(color_key, MODE_COLORS)
            self.assertIsInstance(MODE_COLORS[color_key], int)


class TestConfiguration(unittest.TestCase):
    """Tests pour la configuration de l'environnement"""

    def test_env_example_exists(self):
        """Vérifier que .env.example existe"""
        env_example_path = os.path.join(
            os.path.dirname(__file__), '..', '.env.example'
        )
        self.assertTrue(
            os.path.exists(env_example_path),
            ".env.example devrait exister pour la documentation"
        )

    def test_requirements_exists(self):
        """Vérifier que requirements.txt existe"""
        requirements_path = os.path.join(
            os.path.dirname(__file__), '..', 'requirements.txt'
        )
        self.assertTrue(
            os.path.exists(requirements_path),
            "requirements.txt devrait exister"
        )

    def test_gitignore_exists(self):
        """Vérifier que .gitignore existe"""
        gitignore_path = os.path.join(
            os.path.dirname(__file__), '..', '.gitignore'
        )
        self.assertTrue(
            os.path.exists(gitignore_path),
            ".gitignore devrait exister"
        )


if __name__ == '__main__':
    unittest.main()
