"""
Script de test d'intégration pour vérifier le bon fonctionnement du bot

Ce script vérifie que toutes les composantes du bot fonctionnent ensemble
sans lancer le bot Discord réel.
"""
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.session import SessionManager
from src.utils.ai_client import AIClient
from src.modes.branding_mode import BrandingMode
from src.modes.game_master_mode import GameMasterMode
from src.modes.webradio_mode import WebRadioMode
from src.modes.organisation_mode import OrganisationMode


def test_session_workflow():
    """Test du workflow complet d'une session utilisateur"""
    print("🔄 Test du workflow de session...")

    manager = SessionManager()
    user_id = 12345

    # 1. Créer une session
    session = manager.get_session(user_id)
    assert session.user_id == user_id
    print("  ✅ Session créée")

    # 2. Activer un mode
    mode = BrandingMode()
    mode.set_persona("clara")
    session.set_mode(mode)
    assert session.current_mode is not None
    print("  ✅ Mode activé")

    # 3. Ajouter des messages
    session.add_message("user", "Bonjour")
    session.add_message("assistant", "Salut")
    assert len(session.get_history()) == 2
    print("  ✅ Messages ajoutés à l'historique")

    # 4. Reset session
    manager.reset_session(user_id)
    assert len(session.get_history()) == 0
    print("  ✅ Session réinitialisée")

    print("✅ Test du workflow de session : OK\n")


def test_all_modes_initialization():
    """Test que tous les modes s'initialisent correctement"""
    print("🔄 Test de l'initialisation de tous les modes...")

    modes = [
        ("Branding", BrandingMode()),
        ("Game Master", GameMasterMode()),
        ("WebRadio", WebRadioMode()),
        ("Organisation", OrganisationMode())
    ]

    for name, mode in modes:
        # Vérifier le nom
        mode_name = mode.get_mode_name()
        assert mode_name is not None
        print(f"  ✅ {name}: {mode_name}")

        # Vérifier le prompt système
        if name == "Branding":
            mode.set_persona("clara")
        prompt = mode.get_system_prompt()
        assert prompt is not None
        assert len(prompt) > 0
        print(f"     → Prompt système chargé ({len(prompt)} caractères)")

    print("✅ Test d'initialisation des modes : OK\n")


def test_persona_selection():
    """Test de la sélection de persona pour le mode Branding"""
    print("🔄 Test de la sélection de persona...")

    mode = BrandingMode()
    personas = ["clara", "antoine", "julie"]

    for persona in personas:
        mode_test = BrandingMode()
        mode_test.set_persona(persona)
        assert mode_test.persona_selected
        name = mode_test.get_mode_name()
        assert persona.capitalize() in name
        print(f"  ✅ Persona {persona}: {name}")

    print("✅ Test de sélection de persona : OK\n")


def test_session_validation():
    """Test des validations de session"""
    print("🔄 Test des validations de session...")

    session = SessionManager().get_session(99999)

    # Test validation longueur
    is_valid, error = session.validate_message_length("Message normal")
    assert is_valid is True
    print("  ✅ Message valide accepté")

    is_valid, error = session.validate_message_length("   ")
    assert is_valid is False
    print("  ✅ Message vide rejeté")

    # Test rate limiting
    # Configurer une limite basse
    os.environ['MAX_MESSAGES_PER_MINUTE'] = '2'
    session2 = SessionManager().get_session(88888)

    assert session2.check_rate_limit() is True
    assert session2.check_rate_limit() is True
    assert session2.check_rate_limit() is False  # Dépassement
    print("  ✅ Rate limiting fonctionne")

    # Nettoyer
    del os.environ['MAX_MESSAGES_PER_MINUTE']

    print("✅ Test des validations : OK\n")


def test_ai_client_configuration():
    """Test de la configuration du client IA"""
    print("🔄 Test de la configuration du client IA...")

    # Vérifier que les variables d'environnement nécessaires sont documentées
    env_example_path = os.path.join(os.path.dirname(__file__), '..', '.env.example')
    assert os.path.exists(env_example_path)
    print("  ✅ .env.example existe")

    # Tester la création du client (si les clés sont configurées)
    if os.getenv('OPENAI_API_KEY'):
        try:
            client = AIClient()
            info = client.get_model_info()
            print(f"  ✅ Client IA configuré: {info['provider']} - {info['model']}")
        except Exception as e:
            print(f"  ⚠️  Client IA non disponible: {e}")
    else:
        print("  ℹ️  Clé API non configurée (normal en test)")

    print("✅ Test de configuration du client IA : OK\n")


def main():
    """Exécute tous les tests d'intégration"""
    print("=" * 60)
    print("🧪 TESTS D'INTÉGRATION - Discord Sales Bot")
    print("=" * 60)
    print()

    try:
        test_session_workflow()
        test_all_modes_initialization()
        test_persona_selection()
        test_session_validation()
        test_ai_client_configuration()

        print("=" * 60)
        print("✅ TOUS LES TESTS D'INTÉGRATION ONT RÉUSSI")
        print("=" * 60)
        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ÉCHEC DES TESTS: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
