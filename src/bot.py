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


# Couleurs des modes selon le plan
MODE_COLORS = {
    "branding": 0x3498db,  # Bleu
    "gamemaster": 0x9b59b6,  # Violet
    "webradio": 0xe67e22,  # Orange
    "organisation": 0x2ecc71,  # Vert
    "default": 0x95a5a6,  # Gris
    "error": 0xe74c3c,  # Rouge
    "success": 0x2ecc71,  # Vert
}


def create_embed(title: str, description: str, color_key: str = "default", footer: Optional[str] = None) -> discord.Embed:
    """Crée un embed Discord formaté"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=MODE_COLORS.get(color_key, MODE_COLORS["default"])
    )

    if footer:
        embed.set_footer(text=footer)
    else:
        embed.set_footer(text="Bot d'Entraînement Commercial • Tapez /help pour l'aide")

    return embed


def split_message(message: str, max_length: int = 2000) -> list[str]:
    """
    Découpe un message en plusieurs parties si nécessaire.

    Args:
        message: Le message à découper
        max_length: Longueur maximale par message (défaut: 2000 pour Discord)

    Returns:
        Liste de messages découpés intelligemment
    """
    # Si le message est déjà assez court
    if len(message) <= max_length:
        return [message]

    chunks = []
    current_chunk = ""

    # Découper par paragraphes d'abord (double saut de ligne)
    paragraphs = message.split('\n\n')

    for paragraph in paragraphs:
        # Si le paragraphe seul est trop long, le découper par phrases
        if len(paragraph) > max_length:
            sentences = paragraph.replace('. ', '.\n').split('\n')

            for sentence in sentences:
                # Si une seule phrase est trop longue, découper brutalement
                if len(sentence) > max_length:
                    # Découper en morceaux de max_length
                    for i in range(0, len(sentence), max_length - 3):
                        chunk_part = sentence[i:i + max_length - 3]
                        if i + max_length - 3 < len(sentence):
                            chunk_part += "..."
                        chunks.append(chunk_part)
                    continue

                # Vérifier si on peut ajouter la phrase au chunk actuel
                if len(current_chunk) + len(sentence) + 1 <= max_length:
                    current_chunk += sentence + ' '
                else:
                    # Sauvegarder le chunk actuel et commencer un nouveau
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ' '
        else:
            # Vérifier si on peut ajouter le paragraphe au chunk actuel
            if len(current_chunk) + len(paragraph) + 2 <= max_length:
                current_chunk += paragraph + '\n\n'
            else:
                # Sauvegarder le chunk actuel et commencer un nouveau
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'

    # Ajouter le dernier chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks if chunks else [message[:max_length]]


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

        # Configurer le canal autorisé (optionnel)
        allowed_channel = os.getenv('ALLOWED_CHANNEL_ID', '').strip()
        self.allowed_channel_id = int(allowed_channel) if allowed_channel and allowed_channel.isdigit() else None

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

            # Créer un embed pour le menu de sélection
            embed = create_embed(
                title="🎨 Mode Branding - Sélection de Persona",
                description=(
                    "Choisissez un client à qui présenter votre offre de branding/web/graphisme :\n\n"
                    "**1️⃣ Clara - L'Équilibriste Épuisé·e**\n"
                    "Créatif·ve submergé·e, cherche simplicité et accompagnement.\n"
                    "*Tapez : `clara`*\n\n"
                    "**2️⃣ Antoine - Le Stratège Lucide**\n"
                    "Entrepreneur expérimenté, cherche vision et ROI clair.\n"
                    "*Tapez : `antoine`*\n\n"
                    "**3️⃣ Julie - Le Sceptique Dominant**\n"
                    "Client pressé et exigeant, teste votre autorité.\n"
                    "*Tapez : `julie`*"
                ),
                color_key="branding",
                footer="Choisissez votre persona en tapant son prénom dans le chat"
            )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(name="gamemaster", description="Mode Game Master JDR")
        async def gamemaster_command(interaction: discord.Interaction):
            """Démarre le mode Game Master"""
            session = self.session_manager.get_session(interaction.user.id)

            # Créer et configurer le mode
            mode = GameMasterMode()
            session.set_mode(mode)
            session.conversation_history = []

            embed = create_embed(
                title="🎲 Mode Game Master JDR",
                description=(
                    "**Mode activé avec succès !**\n\n"
                    "Je suis un maître du jeu passionné mais exigeant. "
                    "Présentez-moi vos illustrations JDR générées par IA.\n\n"
                    "Je vais évaluer :\n"
                    "• La valeur narrative et l'immersion\n"
                    "• L'authenticité vs illustrations générées par IA\n"
                    "• Les droits d'usage (réutilisation, impression, projection)\n\n"
                    "**À vous de me convaincre !**"
                ),
                color_key="gamemaster"
            )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(name="webradio", description="Mode Partenaire WebRadio")
        async def webradio_command(interaction: discord.Interaction):
            """Démarre le mode WebRadio"""
            session = self.session_manager.get_session(interaction.user.id)

            # Créer et configurer le mode
            mode = WebRadioMode()
            session.set_mode(mode)
            session.conversation_history = []

            embed = create_embed(
                title="📻 Mode Partenaire WebRadio",
                description=(
                    "**Mode activé avec succès !**\n\n"
                    "Je suis un responsable marketing/annonceur potentiel, orienté ROI. "
                    "Présentez-moi votre webradio et expliquez pourquoi je devrais y investir mon budget publicitaire.\n\n"
                    "Je veux savoir :\n"
                    "• Chiffres d'audience précis et vérifiables\n"
                    "• ROI mesurable comparé à d'autres leviers (réseaux sociaux, Google Ads)\n"
                    "• Métriques de tracking et reporting\n\n"
                    "**Je protège mon budget. Convainquez-moi !**"
                ),
                color_key="webradio"
            )

            await interaction.response.send_message(embed=embed)

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

            embed = create_embed(
                title="📋 Mode Organisation/Productivité",
                description=(
                    f"**Mode activé avec succès !**\n\n"
                    f"{initial_msg}\n\n"
                    "Je suis ultra-sceptique et rationnel. "
                    "J'ai déjà essayé et abandonné : agendas, Notion, Bullet Journal.\n\n"
                    "**Je compare tout à un agenda à 15€. Prouvez-moi que ça vaut le coup !**"
                ),
                color_key="organisation"
            )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(name="reset", description="Réinitialise votre session")
        async def reset_command(interaction: discord.Interaction):
            """Réinitialise la session de l'utilisateur"""
            self.session_manager.reset_session(interaction.user.id)

            embed = create_embed(
                title="🔄 Session Réinitialisée",
                description=(
                    "**Votre session a été réinitialisée avec succès !**\n\n"
                    "Vous pouvez maintenant commencer un nouveau mode d'entraînement :\n\n"
                    "🎨 `/branding` - Clients Web/Graphisme\n"
                    "🎲 `/gamemaster` - Maître du Jeu JDR\n"
                    "📻 `/webradio` - Partenaire WebRadio\n"
                    "📋 `/organisation` - Client Organisation\n\n"
                    "Utilisez `/help` pour plus d'informations."
                ),
                color_key="success"
            )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(name="help", description="Affiche l'aide et les commandes disponibles")
        async def help_command(interaction: discord.Interaction):
            """Affiche l'aide"""
            embed = discord.Embed(
                title="🤖 Bot d'Entraînement Commercial",
                description="Simulateur de clients pénibles pour améliorer vos compétences commerciales",
                color=MODE_COLORS["default"]
            )

            embed.add_field(
                name="📋 Commandes Disponibles",
                value=(
                    "🎨 `/branding` - Clients Web/Graphisme (3 personas)\n"
                    "🎲 `/gamemaster` - Maître du Jeu JDR\n"
                    "📻 `/webradio` - Partenaire WebRadio\n"
                    "📋 `/organisation` - Client Organisation\n"
                    "🔄 `/reset` - Réinitialiser la session\n"
                    "❓ `/help` - Afficher cette aide"
                ),
                inline=False
            )

            embed.add_field(
                name="💡 Comment ça marche ?",
                value=(
                    "**1.** Choisissez un mode avec une commande slash\n"
                    "**2.** Le bot incarnera un client sceptique et exigeant\n"
                    "**3.** Défendez votre produit/service face aux objections\n"
                    "**4.** Recevez un score et des conseils à la fin"
                ),
                inline=False
            )

            embed.add_field(
                name="🎯 Objectif",
                value=(
                    "Améliorer votre pitch, gérer les objections, "
                    "et convaincre même les clients les plus difficiles !"
                ),
                inline=False
            )

            embed.set_footer(text="Bonne chance dans vos entraînements commerciaux !")

            await interaction.response.send_message(embed=embed)

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

        # Afficher le canal autorisé (si configuré)
        if self.allowed_channel_id:
            print(f"📍 Canal autorisé : {self.allowed_channel_id}")
        else:
            print("📍 Tous les canaux sont autorisés")

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

        # Vérifier si le message provient du canal autorisé (si configuré)
        if self.allowed_channel_id and message.channel.id != self.allowed_channel_id:
            return  # Ignorer silencieusement les messages des autres canaux

        # Ignorer et aider pour les commandes slash
        if message.content.startswith('/'):
            # Extraire le nom de la commande
            command_name = message.content.split()[0][1:].lower()
            valid_commands = ["branding", "gamemaster", "webradio", "organisation", "reset", "help"]

            if command_name not in valid_commands:
                embed = create_embed(
                    title="❌ Commande Inconnue",
                    description=(
                        f"La commande `/{command_name}` n'existe pas.\n\n"
                        "**Commandes disponibles :**\n"
                        "• `/branding` - Mode Branding\n"
                        "• `/gamemaster` - Mode Game Master\n"
                        "• `/webradio` - Mode WebRadio\n"
                        "• `/organisation` - Mode Organisation\n"
                        "• `/reset` - Réinitialiser\n"
                        "• `/help` - Aide complète"
                    ),
                    color_key="error"
                )
                await message.reply(embed=embed)
            return

        # Récupérer ou créer la session utilisateur
        session = self.session_manager.get_session(message.author.id)

        # Valider la longueur du message
        is_valid, error_msg = session.validate_message_length(message.content)
        if not is_valid:
            embed = create_embed(
                title="❌ Message Invalide",
                description=f"{error_msg}\n\nVeuillez envoyer un message plus court.",
                color_key="error"
            )
            await message.reply(embed=embed)
            return

        # Vérifier le rate limit
        if not session.check_rate_limit():
            embed = create_embed(
                title="⏰ Ralentissez !",
                description=(
                    "Vous envoyez trop de messages trop rapidement.\n\n"
                    "Veuillez attendre quelques instants avant de réessayer."
                ),
                color_key="error",
                footer="Protection anti-spam • Attendez 1 minute"
            )
            await message.reply(embed=embed)
            return

        # Si pas de mode actif, ignorer
        if not session.current_mode:
            embed = create_embed(
                title="👋 Bienvenue !",
                description=(
                    "Aucun mode n'est actif pour le moment.\n\n"
                    "**Commencez votre entraînement avec l'une de ces commandes :**\n\n"
                    "🎨 `/branding` - Clients Web/Graphisme\n"
                    "🎲 `/gamemaster` - Maître du Jeu JDR\n"
                    "📻 `/webradio` - Partenaire WebRadio\n"
                    "📋 `/organisation` - Client Organisation\n\n"
                    "Utilisez `/help` pour plus d'informations."
                ),
                color_key="default"
            )
            await message.reply(embed=embed)
            return

        # Gérer la sélection de persona pour Branding
        if isinstance(session.current_mode, BrandingMode) and not session.current_mode.persona_selected:
            # L'utilisateur doit sélectionner un persona
            persona_key = BrandingMode.get_persona_key(message.content)

            if persona_key:
                # Sélection valide
                session.current_mode.set_persona(persona_key)

                # Descriptions des personas
                persona_descriptions = {
                    "clara": "Créatif·ve épuisé·e qui cherche simplicité et accompagnement. Je suis submergé·e et j'ai besoin qu'on me guide.",
                    "antoine": "Entrepreneur expérimenté qui cherche vision et ROI clair. Je veux comprendre le vrai impact de votre offre.",
                    "julie": "Client pressé et exigeant qui teste votre autorité. Je n'ai pas de temps à perdre avec du flou."
                }

                embed = create_embed(
                    title=f"✅ Persona : {session.current_mode.get_mode_name()}",
                    description=(
                        f"**Persona activé avec succès !**\n\n"
                        f"{persona_descriptions.get(persona_key, '')}\n\n"
                        "Présentez-moi votre offre de branding. Je vais la challenger."
                    ),
                    color_key="branding"
                )
                await message.reply(embed=embed)
            else:
                # Sélection invalide
                embed = create_embed(
                    title="❌ Persona Invalide",
                    description=(
                        "Veuillez choisir un persona valide :\n\n"
                        "• `clara` - L'Équilibriste Épuisé·e\n"
                        "• `antoine` - Le Stratège Lucide\n"
                        "• `julie` - Le Sceptique Dominant"
                    ),
                    color_key="error"
                )
                await message.reply(embed=embed)
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

            # Logger la réponse de l'IA pour débogage
            print(f"\n{'='*80}")
            print(f"🤖 Réponse IA générée pour {message.author.name}")
            print(f"📏 Longueur : {len(response)} caractères")
            if len(response) > 2000:
                print(f"⚠️  Message long détecté ! Sera découpé en {(len(response) // 2000) + 1} parties")
            print(f"\n📝 RÉPONSE COMPLÈTE :")
            print(f"{'-'*80}")
            print(response)
            print(f"{'-'*80}\n")
            print(f"{'='*80}\n")

            # Ajouter le message utilisateur et la réponse à l'historique
            session.add_message("user", message.content)
            session.add_message("assistant", response)

            # Vérifier si la session doit se terminer (décision prise)
            if session.current_mode.should_end_session(response):
                response += "\n\n✅ **Session terminée !** Utilisez `/reset` pour recommencer."

            # Découper la réponse si elle dépasse 2000 caractères
            message_chunks = split_message(response, max_length=2000)

            # Envoyer le premier message en réponse
            await message.reply(message_chunks[0])

            # Envoyer les messages suivants (s'il y en a) dans le même canal
            for chunk in message_chunks[1:]:
                await message.channel.send(chunk)

        except Exception as e:
            print(f"❌ Erreur lors du traitement du message : {e}")
            import traceback
            traceback.print_exc()

            embed = create_embed(
                title="❌ Erreur",
                description=(
                    "Désolé, une erreur s'est produite lors du traitement de votre message.\n\n"
                    "**Que faire ?**\n"
                    "• Réessayez dans quelques instants\n"
                    "• Si le problème persiste, utilisez `/reset` pour réinitialiser votre session\n"
                    "• Utilisez `/help` pour voir les commandes disponibles"
                ),
                color_key="error"
            )
            await message.reply(embed=embed)


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
