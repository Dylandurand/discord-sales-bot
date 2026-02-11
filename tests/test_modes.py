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
from src.modes.writer_mode import WriterMode


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

        # Messages qui devraient terminer la session (format officiel des prompts)
        self.assertTrue(mode.should_end_session("📊 DÉCISION : ACHAT"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : REFUS"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : HÉSITATION"))

        # Messages normaux de conversation (ne doivent PAS terminer la session)
        self.assertFalse(mode.should_end_session("Pouvez-vous m'en dire plus ?"))

        # IMPORTANT: Mots clés dans le contexte normal (faux positifs à éviter)
        self.assertFalse(mode.should_end_session("Pourquoi ferais-je un achat maintenant ?"))
        self.assertFalse(mode.should_end_session("Je refuse de payer ce prix sans garanties"))
        self.assertFalse(mode.should_end_session("J'hésite beaucoup à m'engager"))
        self.assertFalse(mode.should_end_session("Cet accord ne me convient pas du tout"))


class TestGameMasterMode(unittest.TestCase):
    """Tests pour le mode Game Master"""

    def test_init(self):
        """Test de l'initialisation du mode"""
        mode = GameMasterMode()
        self.assertIsNotNone(mode)
        self.assertFalse(mode.persona_selected)

    def test_persona_selection(self):
        """Test de la sélection de persona"""
        mode = GameMasterMode()

        # Test des clés valides
        self.assertEqual(GameMasterMode.get_persona_key("gael"), "gael")
        self.assertEqual(GameMasterMode.get_persona_key("Gael"), "gael")
        self.assertEqual(GameMasterMode.get_persona_key("LYRA"), "lyra")
        self.assertEqual(GameMasterMode.get_persona_key("lyra"), "lyra")
        self.assertEqual(GameMasterMode.get_persona_key("sylvan"), "sylvan")
        self.assertEqual(GameMasterMode.get_persona_key("SYLVAN"), "sylvan")
        self.assertEqual(GameMasterMode.get_persona_key("Sylvan"), "sylvan")

        # Test des clés invalides
        self.assertIsNone(GameMasterMode.get_persona_key("invalid"))
        self.assertIsNone(GameMasterMode.get_persona_key(""))
        self.assertIsNone(GameMasterMode.get_persona_key("clara"))  # Persona de branding

    def test_set_persona(self):
        """Test de la configuration d'un persona"""
        mode = GameMasterMode()
        mode.set_persona("gael")

        self.assertTrue(mode.persona_selected)
        self.assertIn("Gaël", mode.get_mode_name())

        # Test avec l'autre persona
        mode2 = GameMasterMode()
        mode2.set_persona("lyra")

        self.assertTrue(mode2.persona_selected)
        self.assertIn("Lyra", mode2.get_mode_name())

        # Test avec le persona conservation
        mode3 = GameMasterMode()
        mode3.set_persona("sylvan")

        self.assertTrue(mode3.persona_selected)
        self.assertIn("Sylvan", mode3.get_mode_name())

    def test_set_persona_invalid(self):
        """Test de la configuration d'un persona invalide"""
        mode = GameMasterMode()

        with self.assertRaises(ValueError):
            mode.set_persona("invalid")

    def test_get_mode_name(self):
        """Test du nom du mode"""
        # Sans persona
        mode = GameMasterMode()
        name = mode.get_mode_name()
        self.assertIn("Game Master", name)
        self.assertIn("Sélection", name)

        # Avec persona
        mode.set_persona("gael")
        name = mode.get_mode_name()
        self.assertIn("Game Master", name)
        self.assertIn("Gaël", name)

    def test_get_system_prompt(self):
        """Test du chargement du prompt"""
        mode = GameMasterMode()
        mode.set_persona("gael")

        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés attendus
        self.assertIn("jeu de rôle", prompt.lower())

    def test_get_system_prompt_worldbuilder(self):
        """Test du chargement du prompt worldbuilder"""
        mode = GameMasterMode()
        mode.set_persona("lyra")

        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés du worldbuilder
        self.assertIn("world builder", prompt.lower())

    def test_get_system_prompt_conservation(self):
        """Test du chargement du prompt conservation (Sylvan)"""
        mode = GameMasterMode()
        mode.set_persona("sylvan")

        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés de la conservation
        self.assertIn("conservation", prompt.lower())

    def test_get_initial_message(self):
        """Test du message initial"""
        # Sans persona - devrait retourner le menu avec les trois personas
        mode = GameMasterMode()
        msg = mode.get_initial_message()

        self.assertIsNotNone(msg)
        self.assertIn("gael", msg.lower())
        self.assertIn("lyra", msg.lower())
        self.assertIn("sylvan", msg.lower())

        # Avec persona - devrait retourner None
        mode.set_persona("gael")
        msg = mode.get_initial_message()
        self.assertIsNone(msg)

        # Avec persona Sylvan - devrait aussi retourner None
        mode_sylvan = GameMasterMode()
        mode_sylvan.set_persona("sylvan")
        msg = mode_sylvan.get_initial_message()
        self.assertIsNone(msg)

    def test_is_valid_persona(self):
        """Test de la validation de persona"""
        self.assertTrue(GameMasterMode.is_valid_persona("gael"))
        self.assertTrue(GameMasterMode.is_valid_persona("Gael"))
        self.assertTrue(GameMasterMode.is_valid_persona("LYRA"))
        self.assertTrue(GameMasterMode.is_valid_persona("lyra"))
        self.assertTrue(GameMasterMode.is_valid_persona("sylvan"))
        self.assertTrue(GameMasterMode.is_valid_persona("SYLVAN"))
        self.assertTrue(GameMasterMode.is_valid_persona("Sylvan"))

        self.assertFalse(GameMasterMode.is_valid_persona("invalid"))
        self.assertFalse(GameMasterMode.is_valid_persona(""))
        self.assertFalse(GameMasterMode.is_valid_persona("clara"))

    def test_should_end_session(self):
        """Test de la détection de fin de session"""
        mode = GameMasterMode()

        # Format officiel des prompts
        self.assertTrue(mode.should_end_session("📊 DÉCISION : ACHAT"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : REFUS"))

        # Messages normaux
        self.assertFalse(mode.should_end_session("Question normale"))

        # Faux positifs à éviter
        self.assertFalse(mode.should_end_session("Pourquoi ferais-je un achat sans voir de vraie valeur narrative ?"))
        self.assertFalse(mode.should_end_session("Je refuse de payer pour du générique"))


class TestWriterMode(unittest.TestCase):
    """Tests pour le mode Writer (Écriture)"""

    def test_init(self):
        """Test de l'initialisation du mode"""
        mode = WriterMode()
        self.assertIsNotNone(mode)
        self.assertFalse(mode.persona_selected)

    def test_persona_selection(self):
        """Test de la sélection de persona"""
        # Test des clés valides
        self.assertEqual(WriterMode.get_persona_key("mireille"), "mireille")
        self.assertEqual(WriterMode.get_persona_key("Mireille"), "mireille")
        self.assertEqual(WriterMode.get_persona_key("DAMIEN"), "damien")
        self.assertEqual(WriterMode.get_persona_key("damien"), "damien")
        self.assertEqual(WriterMode.get_persona_key("remi"), "remi")
        self.assertEqual(WriterMode.get_persona_key("REMI"), "remi")
        self.assertEqual(WriterMode.get_persona_key("Remi"), "remi")

        # Test des clés invalides
        self.assertIsNone(WriterMode.get_persona_key("invalid"))
        self.assertIsNone(WriterMode.get_persona_key(""))
        self.assertIsNone(WriterMode.get_persona_key("clara"))   # Persona branding
        self.assertIsNone(WriterMode.get_persona_key("gael"))    # Persona gamemaster

    def test_set_persona(self):
        """Test de la configuration d'un persona"""
        mode = WriterMode()
        mode.set_persona("mireille")

        self.assertTrue(mode.persona_selected)
        self.assertIn("Mireille", mode.get_mode_name())

        # Test avec Damien
        mode2 = WriterMode()
        mode2.set_persona("damien")

        self.assertTrue(mode2.persona_selected)
        self.assertIn("Damien", mode2.get_mode_name())

        # Test avec Rémi
        mode3 = WriterMode()
        mode3.set_persona("remi")

        self.assertTrue(mode3.persona_selected)
        self.assertIn("Rémi", mode3.get_mode_name())

    def test_set_persona_invalid(self):
        """Test de la configuration d'un persona invalide"""
        mode = WriterMode()

        with self.assertRaises(ValueError):
            mode.set_persona("invalid")

    def test_get_mode_name(self):
        """Test du nom du mode"""
        # Sans persona
        mode = WriterMode()
        name = mode.get_mode_name()
        self.assertIn("Écriture", name)
        self.assertIn("Sélection", name)

        # Avec persona Mireille
        mode.set_persona("mireille")
        name = mode.get_mode_name()
        self.assertIn("Écriture", name)
        self.assertIn("Mireille", name)

    def test_get_system_prompt_fantasy(self):
        """Test du chargement du prompt fantasy (Mireille)"""
        mode = WriterMode()
        mode.set_persona("mireille")

        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés du fantasy éditorial
        self.assertIn("fantasy", prompt.lower())

    def test_get_system_prompt_thriller(self):
        """Test du chargement du prompt thriller (Damien)"""
        mode = WriterMode()
        mode.set_persona("damien")

        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés du thriller
        self.assertIn("thriller", prompt.lower())

    def test_get_system_prompt_buyer(self):
        """Test du chargement du prompt acheteur (Rémi)"""
        mode = WriterMode()
        mode.set_persona("remi")

        prompt = mode.get_system_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        # Vérifier que le prompt contient des mots-clés de l'acheteur
        self.assertIn("acheteur", prompt.lower())

    def test_get_initial_message(self):
        """Test du message initial"""
        # Sans persona - devrait retourner le menu avec les trois personas
        mode = WriterMode()
        msg = mode.get_initial_message()

        self.assertIsNotNone(msg)
        self.assertIn("mireille", msg.lower())
        self.assertIn("damien", msg.lower())
        self.assertIn("remi", msg.lower())

        # Avec persona - devrait retourner None
        mode.set_persona("mireille")
        msg = mode.get_initial_message()
        self.assertIsNone(msg)

        # Avec persona Rémi - devrait aussi retourner None
        mode_remi = WriterMode()
        mode_remi.set_persona("remi")
        msg = mode_remi.get_initial_message()
        self.assertIsNone(msg)

    def test_is_valid_persona(self):
        """Test de la validation de persona"""
        self.assertTrue(WriterMode.is_valid_persona("mireille"))
        self.assertTrue(WriterMode.is_valid_persona("Mireille"))
        self.assertTrue(WriterMode.is_valid_persona("DAMIEN"))
        self.assertTrue(WriterMode.is_valid_persona("damien"))
        self.assertTrue(WriterMode.is_valid_persona("remi"))
        self.assertTrue(WriterMode.is_valid_persona("REMI"))
        self.assertTrue(WriterMode.is_valid_persona("Remi"))

        self.assertFalse(WriterMode.is_valid_persona("invalid"))
        self.assertFalse(WriterMode.is_valid_persona(""))
        self.assertFalse(WriterMode.is_valid_persona("clara"))
        self.assertFalse(WriterMode.is_valid_persona("gael"))

    def test_should_end_session(self):
        """Test de la détection de fin de session"""
        mode = WriterMode()

        # Format officiel des prompts
        self.assertTrue(mode.should_end_session("📊 DÉCISION : ACCEPTATION SOUS RÉSERVE"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : REFUS"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : RÉÉCRITURE DEMANDÉE"))

        # Messages normaux
        self.assertFalse(mode.should_end_session("Intéressant, continuez..."))

        # Faux positifs à éviter
        self.assertFalse(mode.should_end_session("Pourquoi un acheteur choisirait ce livre ?"))
        self.assertFalse(mode.should_end_session("Je refuse de croire que ça fonctionnera en librairie"))

    def test_init_with_persona(self):
        """Test de l'initialisation directe avec un persona"""
        mode = WriterMode(persona_key="damien")

        self.assertTrue(mode.persona_selected)
        self.assertEqual(mode.persona_key, "damien")
        self.assertIn("Damien", mode.get_mode_name())

    def test_init_with_invalid_persona(self):
        """Test de l'initialisation avec un persona invalide"""
        with self.assertRaises(ValueError):
            WriterMode(persona_key="unknown")


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

        # Format officiel des prompts
        self.assertTrue(mode.should_end_session("📊 DÉCISION : REFUS"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : ACCORD"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : INTÉRÊT CONDITIONNEL"))

        # Messages normaux
        self.assertFalse(mode.should_end_session("Message normal"))

        # Faux positifs à éviter
        self.assertFalse(mode.should_end_session("Un accord de partenariat nécessite des données vérifiables"))
        self.assertFalse(mode.should_end_session("Je refuse de m'engager sans chiffres concrets"))


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

        # Format officiel des prompts
        self.assertTrue(mode.should_end_session("📊 DÉCISION : ACHÈTE"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : N'ACHÈTE PAS"))
        self.assertTrue(mode.should_end_session("📊 DÉCISION : HÉSITE"))

        # Messages normaux
        self.assertFalse(mode.should_end_session("Hmm, intéressant..."))

        # Faux positifs à éviter
        self.assertFalse(mode.should_end_session("J'hésite beaucoup à investir dans un autre outil"))
        self.assertFalse(mode.should_end_session("Pourquoi n'achète-t-on pas plutôt un simple agenda ?"))


class TestPromptFiles(unittest.TestCase):
    """Tests pour vérifier que tous les fichiers de prompts existent"""

    def test_branding_prompts_exist(self):
        """Vérifier que les prompts Branding existent"""
        prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'prompts')

        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'branding_clara.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'branding_antoine.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'branding_julie.md')))

    def test_game_master_prompts_exist(self):
        """Vérifier que les prompts Game Master existent"""
        prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'prompts')

        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'game_master.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'game_master_worldbuilder.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'game_master_conservation.md')))

    def test_writer_prompts_exist(self):
        """Vérifier que les prompts Writer existent"""
        prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'prompts')

        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'ecriture_fantasy.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'ecriture_thriller.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'acheteur_roman_thriller_fantasy.md')))

    def test_other_prompts_exist(self):
        """Vérifier que les autres prompts existent"""
        prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'prompts')

        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'webradio.md')))
        self.assertTrue(os.path.exists(os.path.join(prompts_dir, 'organisation.md')))


if __name__ == '__main__':
    unittest.main()
