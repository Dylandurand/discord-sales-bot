# 🎯 Discord Sales Challenge Bot

Un bot Discord d'entraînement commercial alimenté par l'IA qui simule des clients difficiles pour améliorer vos compétences de vente.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-7289DA.svg)
![Tests](https://img.shields.io/badge/Tests-54%20passing-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Fonctionnalités

- 🎭 **4 modes de clients réalistes** avec personnalités distinctes
- 🤖 **IA conversationnelle** (OpenAI GPT-4/3.5 ou Claude)
- 🎨 **Interface Discord moderne** avec embeds colorés
- 📊 **Système de scoring** intégré dans chaque mode
- 🔒 **Protection anti-spam** et rate limiting
- 💾 **Gestion de sessions** multi-utilisateurs
- ✅ **Tests complets** (54 tests unitaires + tests d'intégration)

## 📋 Description

Ce bot vous permet de vous entraîner à vendre vos services face à 4 types de clients différents, chacun avec sa propre personnalité et ses objections spécifiques :

### 🎨 Mode 1 : Branding/Web/Graphisme
Choisissez parmi 3 personas :
- **Clara** - L'Équilibriste Épuisé·e : Créatif·ve submergé·e, cherche simplicité
- **Antoine** - Le Stratège Lucide : Entrepreneur expérimenté, veut du ROI
- **Julie** - Le Sceptique Dominant : Client pressé qui teste votre autorité

### 🎲 Mode 2 : Game Master JDR
Choisissez parmi 3 personas :
- **Gaël** - LE MAÎTRE EXIGEANT 🎲 : MJ expérimenté, cherche immersion et valeur narrative concrète
- **Lyra** - LA BÂTISSEUSE D'UNIVERS 🌍 : Worldbuilder narratif, cherche cohérence du lore et outils multi-sensoriels
- **Sylvan** - LE GARDIEN DU VIVANT 🌿 : World Builder conservation, ancre les créatures dans le vivant menacé

### 📻 Mode 3 : Partenaire WebRadio
Responsable marketing orienté ROI qui veut des chiffres d'audience précis et des métriques de tracking avant d'investir son budget.

### 📋 Mode 4 : Client Organisation/Productivité
Ultra-sceptique et rationnel qui a déjà essayé (et abandonné) tous les outils. Compare tout à un agenda à 15€.

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- Un compte Discord
- Une clé API OpenAI (GPT-4 ou GPT-3.5-turbo recommandé)

### Configuration

1. **Clonez le repository** :
```bash
git clone https://github.com/VOTRE_USERNAME/discord-sales-bot.git
cd discord-sales-bot
```

2. **Créez un environnement virtuel** :
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installez les dépendances** :
```bash
pip install -r requirements.txt
```

4. **Configurez les variables d'environnement** :
```bash
cp .env.example .env
# Éditez le fichier .env avec vos tokens
```

Exemple de configuration `.env` :
```env
# Discord Configuration
DISCORD_BOT_TOKEN=votre_token_discord_ici

# AI Configuration
AI_PROVIDER=openai
OPENAI_API_KEY=votre_clé_openai_ici
OPENAI_MODEL=gpt-4-turbo-preview

# Optional Settings
AI_TEMPERATURE=0.85
MAX_CONVERSATION_HISTORY=20
SESSION_TIMEOUT_MINUTES=60
MAX_MESSAGES_PER_MINUTE=10
MAX_MESSAGE_LENGTH=2000
```

5. **Créez votre bot Discord** :
   - Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Créez une nouvelle application
   - Dans l'onglet "Bot" :
     - Créez un bot
     - Activez **MESSAGE CONTENT INTENT** ⚠️ (obligatoire)
     - Copiez le token dans `.env`
   - Dans l'onglet "OAuth2" → "URL Generator" :
     - Sélectionnez les scopes : `bot`, `applications.commands`
     - Sélectionnez les permissions : `Send Messages`, `Read Messages/View Channels`, `Use Slash Commands`
     - Copiez l'URL générée et invitez le bot sur votre serveur

6. **Obtenez votre clé API** :
   - OpenAI : [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Claude (alternatif) : [console.anthropic.com](https://console.anthropic.com)

## 🎮 Utilisation

### Démarrer le bot

```bash
python main.py
```

Vous devriez voir :
```
🚀 Lancement du bot...
✅ Bot connecté en tant que VotreBot#1234
📊 Connecté à 1 serveur(s)
🤖 Modèle IA : gpt-4-turbo-preview (openai)
🔄 Synchronisation des commandes slash...
✅ Toutes les commandes sont prêtes !
```

### Commandes disponibles

| Commande | Description | Couleur |
|----------|-------------|---------|
| `/branding` | Mode Branding avec sélection de persona | 🔵 Bleu |
| `/gamemaster` | Mode Game Master JDR | 🟣 Violet |
| `/webradio` | Mode Partenaire WebRadio | 🟠 Orange |
| `/organisation` | Mode Organisation/Productivité | 🟢 Vert |
| `/reset` | Réinitialise votre session | ⚪ Gris |
| `/help` | Affiche l'aide complète | ⚪ Gris |

### Exemple de session

1. Tapez `/branding` pour commencer
2. Choisissez un persona (`clara`, `antoine`, ou `julie`)
3. Présentez votre offre de branding
4. Le client va challenger vos arguments avec des objections réalistes
5. Répondez aux objections et défendez votre proposition
6. Recevez une décision finale et un score

## 💡 Conseils d'utilisation

- ✅ **Posez des questions** pour comprendre les vrais besoins du client
- ✅ **Écoutez les objections** et répondez avec des preuves concrètes
- ✅ **Proposez de la valeur**, pas juste un prix
- ✅ **Restez professionnel** même face à un client difficile
- ✅ **Utilisez `/reset`** pour recommencer un exercice
- ✅ **Analysez les scores** pour identifier vos axes d'amélioration

## 📁 Structure du projet

```
discord-sales-bot/
├── src/
│   ├── bot.py                  # Bot principal et commandes slash
│   ├── modes/                  # Modes de clients
│   │   ├── base_mode.py        # Classe abstraite
│   │   ├── branding_mode.py    # Mode Branding (3 personas)
│   │   ├── game_master_mode.py # Mode Game Master
│   │   ├── webradio_mode.py    # Mode WebRadio
│   │   └── organisation_mode.py# Mode Organisation
│   ├── prompts/                # Prompts RCT (Rôle, Contexte, Tâche)
│   │   ├── branding_clara.md
│   │   ├── branding_antoine.md
│   │   ├── branding_julie.md
│   │   ├── game_master.md              # Gaël - LE MAÎTRE EXIGEANT
│   │   ├── game_master_worldbuilder.md # Lyra - LA BÂTISSEUSE D'UNIVERS
│   │   ├── game_master_conservation.md # Sylvan - LE GARDIEN DU VIVANT
│   │   ├── webradio.md
│   │   └── organisation.md
│   └── utils/                  # Utilitaires
│       ├── ai_client.py        # Client API IA
│       └── session.py          # Gestion des sessions
├── tests/                      # Tests
│   ├── test_session.py         # Tests SessionManager
│   ├── test_modes.py           # Tests des modes
│   ├── test_utils.py           # Tests utilitaires
│   └── integration_test.py     # Tests d'intégration
├── main.py                     # Point d'entrée
├── requirements.txt            # Dépendances Python
├── .env.example                # Template de configuration
├── .gitignore                  # Fichiers ignorés par Git
└── PLAN_DEV_BOT_DISCORD.md    # Plan de développement complet
```

## 🔧 Configuration avancée

### Modèles IA supportés

- **OpenAI** : `gpt-4-turbo-preview`, `gpt-4`, `gpt-3.5-turbo`
- **Claude** : `claude-3-opus`, `claude-3-sonnet` (décommenter dans requirements.txt)

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DISCORD_BOT_TOKEN` | Token du bot Discord | *Obligatoire* |
| `AI_PROVIDER` | Fournisseur IA (`openai` ou `anthropic`) | `openai` |
| `OPENAI_API_KEY` | Clé API OpenAI | *Obligatoire si OpenAI* |
| `OPENAI_MODEL` | Modèle OpenAI à utiliser | `gpt-4-turbo-preview` |
| `AI_TEMPERATURE` | Créativité des réponses (0.0-1.0) | `0.85` |
| `MAX_CONVERSATION_HISTORY` | Nombre de messages conservés | `20` |
| `SESSION_TIMEOUT_MINUTES` | Timeout de session inactif | `60` |
| `MAX_MESSAGES_PER_MINUTE` | Limite anti-spam par utilisateur | `10` |
| `MAX_MESSAGE_LENGTH` | Longueur max d'un message | `2000` |

## 🧪 Tests

### Lancer les tests unitaires

```bash
source venv/bin/activate
python -m unittest discover tests -v
```

Résultat attendu : **54 tests passing** ✅

### Lancer les tests d'intégration

```bash
python tests/integration_test.py
```

### Couverture des tests

- ✅ SessionManager (création, reset, expiration, rate limiting)
- ✅ Tous les modes (initialisation, prompts, fin de session)
- ✅ Validation des messages et rate limiting
- ✅ Configuration du client IA
- ✅ Workflow complet de session

## 📊 Gestion des erreurs

Le bot gère automatiquement :

- ❌ **Messages trop longs** : Limite configurable (2000 caractères par défaut)
- ❌ **Rate limiting** : Protection anti-spam (10 messages/minute par défaut)
- ❌ **Commandes invalides** : Redirection automatique vers `/help`
- ❌ **Messages système Discord** : Filtrés automatiquement
- ❌ **Erreurs API** : Retry automatique et messages d'erreur clairs
- ❌ **Interactions Discord expirées** : Gestion silencieuse des tokens stale (erreur 10062)

## 📝 Développement

### Contribuer

Les contributions sont les bienvenues ! Consultez `PLAN_DEV_BOT_DISCORD.md` pour le plan de développement complet.

**Phases complétées** :
- ✅ Phase 1-7 : Configuration, architecture, modes, API IA
- ✅ Phase 8 : Interface Discord avec embeds et gestion d'erreurs
- ✅ Phase 9 : Tests unitaires et d'intégration
- ✅ Phase 10 : Système de personas multi-niveaux pour Game Master (Gaël, Lyra, Sylvan)

**Prochaines étapes** :
- 📋 Phase 11 : Documentation et déploiement
- 🚀 Phase 12 : Fonctionnalités avancées (statistiques, leaderboard)

### Ajouter un nouveau mode

1. Créez une classe dans `src/modes/` qui hérite de `BaseMode`
2. Créez le prompt RCT dans `src/prompts/`
3. Ajoutez la commande slash dans `src/bot.py`
4. Ajoutez des tests dans `tests/test_modes.py`

## 🚀 Déploiement

### Options d'hébergement

- **VPS** (Recommandé) : OVH, DigitalOcean, Linode
- **Cloud** : Railway, Heroku, AWS EC2
- **Gratuit** : Replit (avec limitations)

### Exemple de déploiement sur VPS

```bash
# Sur votre serveur
git clone https://github.com/VOTRE_USERNAME/discord-sales-bot.git
cd discord-sales-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurez .env
nano .env

# Lancez avec screen ou tmux
screen -S salesbot
python main.py
# Ctrl+A puis D pour détacher
```

### Monitoring

Le bot affiche dans la console :
- ✅ Connexion établie
- 📊 Nombre de serveurs
- 🤖 Modèle IA utilisé
- 🔄 Synchronisation des commandes

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- Inspiré par [chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)
- Propulsé par [discord.py](https://github.com/Rapptz/discord.py)
- IA fournie par [OpenAI](https://openai.com)

## 📞 Support

Pour toute question ou problème :
- 🐛 Ouvrez une [issue sur GitHub](https://github.com/VOTRE_USERNAME/discord-sales-bot/issues)
- 📧 Contactez l'équipe de développement
- 💬 Rejoignez notre serveur Discord de support

---

**Bon courage pour vos entraînements de vente ! 🚀**

*Ce bot est un outil d'entraînement. Les situations simulées sont volontairement difficiles pour vous challenger. Ne prenez pas les critiques personnellement - c'est justement le but de l'exercice !*
