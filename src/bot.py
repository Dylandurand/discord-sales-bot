"""
Bot Discord - Initialisation et gestion des événements
"""
import os
import discord
from discord import app_commands
from typing import Optional

from .utils.session import SessionManager
from .utils.ai_client import AIClient
from .modes.branding_mode import BrandingMode
from .modes.game_master_mode import GameMasterMode
from .modes.webradio_mode import WebRadioMode
from .modes.organisation_mode import OrganisationMode


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

        # Enregistrer les commandes
        self._register_commands()

    def _register_commands(self):
        """Enregistre toutes les commandes slash"""

        @self.tree.command(name="branding", description="Mode Branding avec sélection de persona")
        async def branding_command(interaction: discord.Interaction):
            """Démarre le mode Branding avec menu de sélection de persona"""
            session = self.session_manager.get_session(interaction.user.id)

            # Créer un mode Branding sans persona (affichera le menu)
            branding_mode = BrandingMode()
            session.set_mode(branding_mode)
            session.conversation_history = []  # Reset history

            # Envoyer le menu de sélection
            menu = BrandingMode.get_persona_selection_message()
            await interaction.response.send_message(menu)

        @self.tree.command(name="gamemaster", description="Mode Game Master JDR")
        async def gamemaster_command(interaction: discord.Interaction):
            """Démarre le mode Game Master"""
            session = self.session_manager.get_session(interaction.user.id)

            # Créer et configurer le mode
            mode = GameMasterMode()
            session.set_mode(mode)
            session.conversation_history = []

            await interaction.response.send_message(
                f"🎭 **Mode activé : {mode.get_mode_name()}**\n\n"
                "Présentez vos illustrations JDR générées par IA. "
                "Je vais évaluer leur pertinence pour mes campagnes."
            )

        @self.tree.command(name="webradio", description="Mode Partenaire WebRadio")
        async def webradio_command(interaction: discord.Interaction):
            """Démarre le mode WebRadio"""
            session = self.session_manager.get_session(interaction.user.id)

            # Créer et configurer le mode
            mode = WebRadioMode()
            session.set_mode(mode)
            session.conversation_history = []

            await interaction.response.send_message(
                f"🎭 **Mode activé : {mode.get_mode_name()}**\n\n"
                "Présentez-moi votre webradio et expliquez pourquoi je devrais y investir mon budget publicitaire."
            )

        @self.tree.command(name="organisation", description="Mode Client Organisation/Productivité (Plan Bzz)")
        async def organisation_command(interaction: discord.Interaction):
            """Démarre le mode Organisation"""
            session = self.session_manager.get_session(interaction.user.id)

            # Créer et configurer le mode
            mode = OrganisationMode()
            session.set_mode(mode)
            session.conversation_history = []

            # Ce mode a un message d'ouverture prédéfini
            initial_msg = mode.get_initial_message()

            await interaction.response.send_message(
                f"🎭 **Mode activé : {mode.get_mode_name()}**\n\n{initial_msg}"
            )

        @self.tree.command(name="reset", description="Réinitialise votre session")
        async def reset_command(interaction: discord.Interaction):
            """Réinitialise la session de l'utilisateur"""
            self.session_manager.reset_session(interaction.user.id)
            await interaction.response.send_message(
                "✅ Session réinitialisée ! Utilisez `/branding`, `/gamemaster`, `/webradio` ou `/organisation` pour commencer."
            )

        @self.tree.command(name="help", description="Affiche l'aide et les commandes disponibles")
        async def help_command(interaction: discord.Interaction):
            """Affiche l'aide"""
            help_text = """
# 🤖 Bot d'Entraînement Commercial

Ce bot simule des clients pénibles pour vous aider à améliorer vos compétences commerciales.

## 📋 Commandes disponibles :

- `/branding` - Mode Branding avec 3 personas (Clara, Antoine, Julie)
- `/gamemaster` - Mode Game Master JDR (illustrations IA)
- `/webradio` - Mode Partenaire WebRadio (sponsoring)
- `/organisation` - Mode Client Organisation/Productivité (Plan Bzz)
- `/reset` - Réinitialise votre session
- `/help` - Affiche cette aide

## 💡 Comment ça marche ?

1. Choisissez un mode avec une commande slash
2. Le bot incarnera un client sceptique et exigeant
3. Défendez votre produit/service face aux objections
4. Recevez un score et des conseils à la fin

## 🎯 Objectif :

Améliorer votre pitch, gérer les objections, et convaincre même les clients les plus difficiles !
"""
            await interaction.response.send_message(help_text)

    async def setup_hook(self):
        """Configuration initiale du bot"""
        # La synchronisation des commandes se fait dans on_ready()
        # car self.guilds n'est pas encore disponible ici
        pass

    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        print(f"✅ Bot connecté en tant que {self.user}")
        print(f"📊 Connecté à {len(self.guilds)} serveur(s)")

        # Afficher les informations du modèle IA
        model_info = self.ai_client.get_model_info()
        print(f"🤖 Modèle IA : {model_info['model']} ({model_info['provider']})")

        # Synchroniser les commandes slash avec Discord (par serveur = instantané)
        print("🔄 Synchronisation des commandes slash...")

        # Vérifier combien de commandes sont enregistrées
        commands = self.tree.get_commands()
        print(f"📝 {len(commands)} commandes globales enregistrées : {[cmd.name for cmd in commands]}")

        # Synchroniser par serveur (copie les commandes globales vers chaque serveur)
        for guild in self.guilds:
            # Copier les commandes globales vers ce serveur
            self.tree.copy_global_to(guild=guild)
            # Synchroniser avec Discord
            synced = await self.tree.sync(guild=guild)
            print(f"  ✅ Serveur '{guild.name}' : {len(synced)} commandes synchronisées")

        print("✅ Toutes les commandes sont prêtes !")

    async def on_message(self, message: discord.Message):
        """Événement déclenché à chaque message"""
        # Ignorer les messages du bot lui-même
        if message.author == self.user:
            return

        # Ignorer les messages des autres bots
        if message.author.bot:
            return

        # Ignorer les messages système (ajout de bot, pins, etc.)
        if message.type != discord.MessageType.default and message.type != discord.MessageType.reply:
            return

        # Ignorer les messages qui sont des commandes
        if message.content.startswith('/'):
            return

        # Récupérer ou créer la session utilisateur
        session = self.session_manager.get_session(message.author.id)

        # Si pas de mode actif, ignorer
        if not session.current_mode:
            await message.reply(
                "👋 Utilisez `/help` pour voir les modes disponibles !\n"
                "Commencez par `/branding`, `/gamemaster`, `/webradio` ou `/organisation`"
            )
            return

        # Gérer la sélection de persona pour Branding
        if isinstance(session.current_mode, BrandingMode) and not session.current_mode.persona_selected:
            # L'utilisateur doit sélectionner un persona
            persona_key = BrandingMode.get_persona_key(message.content)

            if persona_key:
                # Sélection valide
                session.current_mode.set_persona(persona_key)
                await message.reply(
                    f"✅ **Persona sélectionné : {session.current_mode.get_mode_name()}**\n\n"
                    "Présentez votre offre de branding. Je vais la challenger."
                )
            else:
                # Sélection invalide
                await message.reply(
                    "❌ Persona invalide. Veuillez choisir : `clara`, `antoine`, ou `julie`"
                )
            return

        # Traiter le message avec le mode actif
        try:
            # Afficher l'indicateur "en train d'écrire..."
            async with message.channel.typing():
                # Utiliser la méthode handle_message du mode
                response = await session.current_mode.handle_message(
                    user_message=message.content,
                    conversation_history=session.get_history(),
                    ai_client=self.ai_client
                )

            # Ajouter le message utilisateur et la réponse à l'historique
            session.add_message("user", message.content)
            session.add_message("assistant", response)

            # Vérifier si la session doit se terminer (décision prise)
            if session.current_mode.should_end_session(response):
                response += "\n\n✅ **Session terminée !** Utilisez `/reset` pour recommencer."

            # Envoyer la réponse
            await message.reply(response)

        except Exception as e:
            print(f"❌ Erreur lors du traitement du message : {e}")
            import traceback
            traceback.print_exc()
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
