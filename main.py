#!/usr/bin/env python3
"""
Discord Sales Challenge Bot - Point d'entrée principal
"""
import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def check_environment():
    """Vérifie que toutes les variables d'environnement nécessaires sont définies"""
    required_vars = ['DISCORD_BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Erreur : Variables d'environnement manquantes :")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Consultez le fichier .env.example pour la configuration.")
        sys.exit(1)

    # Vérifier qu'au moins un provider IA est configuré
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Erreur : Aucune clé API IA configurée.")
        print("   Configurez au moins OPENAI_API_KEY ou ANTHROPIC_API_KEY dans .env")
        sys.exit(1)

def main():
    """Fonction principale"""
    print("🎯 Discord Sales Challenge Bot")
    print("=" * 50)

    # Vérifier l'environnement
    check_environment()

    print("✅ Configuration validée")
    print("🚀 Démarrage du bot...")

    # Importer et démarrer le bot
    from src.bot import start_bot
    start_bot()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt du bot...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        sys.exit(1)
