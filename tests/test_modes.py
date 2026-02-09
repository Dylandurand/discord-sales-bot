"""
Tests unitaires pour les modes de jeu
"""
import unittest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modes.branding_mode import BrandingMode
from src.modes.game_master_mode import GameMasterMode
from src.modes.webradio_mode import WebRadioMode
from src.modes.organisation_mode import OrganisationMode


class TestBrandingMode(unittest.TestCase):
    """Tests pour le mode Branding"""

    def test_init(self):
        """Test de l'initialisation du mode"""
        mode = BrandingMode()
        self.assertIsNotNone(mode)
        self.assertFalse(mode.persona_selected)

    def test_persona_selection(self):
        """Test de la sélection de persona"""
        mode = BrandingMode()

        # Test des clés valides
        self.assertEqual(BrandingMode.get_persona_key("clara"), "clara")
        self.assertEqual(BrandingMode.get_persona_key("Clara"), "clara")
        self.assertEqual(BrandingMode.get_persona_key("ANTOINE"), "antoine")
        self.assertEqual(BrandingMode.get_persona_key("julie"), "julie")

        # Test des clés invalides
        self.assertIsNone(BrandingMode.get_persona_key("invalid"))
        self.assertIsNone(BrandingMode.get_persona_key(""))

    def test_set_persona(self):
        """Test de la configuration d'un persona"""
        mode = BrandingMode()
        mode.set_persona("clara")

        self.assertTrue(mode.persona_selected)
        self.assertIn("Clara", mode.get_mode_name())

    def test_get_system_prompt(self):
        """Test du chargement du prompt système"""
        mode = BrandingMode()
        mode.set_persona("clara")

        prompt = mode.get_system_prompt()
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_should_end_session(self):
        """Test de la détection de fin de session"""
        mode = BrandingMode()

        # Messages qui devraient terminer la session
        self.assertTrue(mode.should_end_session("DÉCISION FINALE : ACHAT"))
        self.assertTrue(mode.should_end_session("DÉCISION FINALE : REFUS"))

        # Messages normaux
        self.assertFalse(mode.should_end_session("Pouvez-vous m'en dire plus ?"))


class TestGameMasterMode(unittest.TestCase):
    """Tests pour le mode Game Master"""

    def test_init(self):
        """Test de l'initialisation"""
        mode = GameMasterMode()
        self.assertIsNotNone(mode)

    def test_get_mode_name(self):
        """Test du nom du mode"""
        mode = GameMasterMode()
        name = mode.get_mode_name()
        self.assertIn("Game Master", name)

    def test_get_system_prompt(self):
        """Test du chargement du prompt"""
        mode = GameMasterMode()
        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés attendus
        self.assertIn("jeu de rôle", prompt.lower())

    def test_should_end_session(self):
        """Test de la détection de fin de session"""
        mode = GameMasterMode()

        self.assertTrue(mode.should_end_session("DÉCISION FINALE : ACHAT"))
        self.assertTrue(mode.should_end_session("DÉCISION FINALE : REFUS"))
        self.assertFalse(mode.should_end_session("Question normale"))


class TestWebRadioMode(unittest.TestCase):
    """Tests pour le mode WebRadio"""

    def test_init(self):
        """Test de l'initialisation"""
        mode = WebRadioMode()
        self.assertIsNotNone(mode)

    def test_get_mode_name(self):
        """Test du nom du mode"""
        mode = WebRadioMode()
        name = mode.get_mode_name()
        self.assertIn("WebRadio", name)

    def test_get_system_prompt(self):
        """Test du chargement du prompt"""
        mode = WebRadioMode()
        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_should_end_session(self):
        """Test de la détection de fin de session"""
        mode = WebRadioMode()

        self.assertTrue(mode.should_end_session("DÉCISION FINALE : REFUS"))
        self.assertTrue(mode.should_end_session("DÉCISION FINALE : ACCORD"))
        self.assertTrue(mode.should_end_session("DÉCISION FINALE : INTÉRÊT CONDITIONNEL"))
        self.assertFalse(mode.should_end_session("Message normal"))


class TestOrganisationMode(unittest.TestCase):
    """Tests pour le mode Organisation"""

    def test_init(self):
        """Test de l'initialisation"""
        mode = OrganisationMode()
        self.assertIsNotNone(mode)

    def test_get_mode_name(self):
        """Test du nom du mode"""
        mode = OrganisationMode()
        name = mode.get_mode_name()
        self.assertIn("Organisation", name)

    def test_get_initial_message(self):
        """Test du message d'ouverture"""
        mode = OrganisationMode()
        msg = mode.get_initial_message()

        self.assertIsNotNone(msg)
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 0)

    def test_get_system_prompt(self):
        """Test du chargement du prompt"""
        mode = OrganisationMode()
        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_should_end_session(self):
        """Test de la détection de fin de session"""
        mode = OrganisationMode()

        self.assertTrue(mode.should_end_session("DÉCISION FINALE : ACHAT"))
        self.assertTrue(mode.should_end_session("DÉCISION FINALE : REFUS"))
        self.assertFalse(mode.should_end_session("Hmm, intéressant..."))


class TestPromptFiles(unittest.TestCase):
    """Tests pour vérifier que tous les fichiers de prompts existent"""

    def test_branding_prompts_exist(self):
        """Vérifier que les prompts Branding existent"""
        prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'prompts')

        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'branding_clara.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'branding_antoine.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'branding_julie.md')))

    def test_other_prompts_exist(self):
        """Vérifier que les autres prompts existent"""
        prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'prompts')

        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'game_master.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'webradio.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'organisation.md')))


if __name__ == '__main__':
    unittest.main()
