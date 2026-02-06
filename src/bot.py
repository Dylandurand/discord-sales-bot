"""
Bot Discord - Initialisation et gestion des événements
"""
import os
import discord
from discord import app_commands
from typing import Optional

from .utils.session import SessionManager
from .utils.ai_client import AIClient


class SalesChallengeBot(discord.Client):
    """Bot Discord pour l'entraînement commercial"""
    
    def __init__(self):
        # Configurer les intents nécessaires
        intents = discord.Intents.default()
        intents.message_content = True  # Nécessaire pour lire les messages
        
        super().__init__(intents=intents)
        
        # Initialiser le gestionnaire de sessions et le client IA
        self.session_manager = SessionManager()
        self.ai_client = AIClient()
        
        # Initialiser l'arbre de commandes slash
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        """Configuration initiale du bot"""
        # Synchroniser les commandes slash avec Discord
        await self.tree.sync()
        print("✅ Commandes slash synchronisées")
        
    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        print(f"✅ Bot connecté en tant que {self.user}")
        print(f"📊 Connecté à {len(self.guilds)} serveur(s)")
        
        # Afficher les informations du modèle IA
        model_info = self.ai_client.get_model_info()
        print(f"🤖 Modèle IA : {model_info['model']} ({model_info['provider']})")
        
    async def on_message(self, message: discord.Message):
        """Événement déclenché à chaque message"""
        # Ignorer les messages du bot lui-même
        if message.author == self.user:
            return
        
        # Ignorer les messages qui sont des commandes
        if message.content.startswith('/'):
            return
            
        # Récupérer ou créer la session utilisateur
        session = self.session_manager.get_session(message.author.id)
        
        # Ajouter le message de l'utilisateur à l'historique
        session.add_message("user", message.content)
        
        try:
            # Afficher l'indicateur "en train d'écrire..."
            async with message.channel.typing():
                # Générer la réponse avec l'IA
                response = await self.ai_client.generate_response(
                    messages=session.get_history(),
                    max_tokens=500,
                    temperature=0.8
                )
            
            # Ajouter la réponse à l'historique
            session.add_message("assistant", response)
            
            # Envoyer la réponse
            await message.reply(response)
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement du message : {e}")
            await message.reply(
                "❌ Désolé, une erreur s'est produite. Réessayez dans quelques instants."
            )


def create_bot() -> SalesChallengeBot:
    """Crée et configure le bot"""
    return SalesChallengeBot()


def start_bot():
    """Démarre le bot Discord"""
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN non défini dans .env")
    
    bot = create_bot()
    
    # TODO: Enregistrer les commandes slash
    # from .commands import register_commands
    # register_commands(bot)
    
    print("🚀 Lancement du bot...")
    bot.run(token)
