# 🎯 Discord Sales Challenge Bot

Un bot Discord d'entraînement commercial qui simule des clients difficiles pour améliorer vos compétences de vente.

## 📋 Description

Ce bot vous permet de vous entraîner à vendre vos services face à 4 types de clients différents :

1. **Mode Branding** - Client cherchant des services de branding/web/graphisme
2. **Mode Game Master** - Maître du jeu cherchant des illustrations pour son jeu de rôle
3. **Mode Webradio** - Partenaire commercial cherchant à faire de la publicité
4. **Mode Organisation** - Client avec des problèmes d'organisation et de productivité

Chaque client est volontairement "pénible" et proche de son argent pour vous challenger !

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- Un compte Discord
- Une clé API OpenAI (ou Claude)

### Configuration

1. Clonez le repository :
```bash
git clone https://github.com/VOTRE_USERNAME/discord-sales-bot.git
cd discord-sales-bot
```

2. Créez un environnement virtuel :
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement :
```bash
cp .env.example .env
# Éditez le fichier .env avec vos tokens
```

5. Créez votre bot Discord :
   - Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Créez une nouvelle application
   - Créez un bot dans l'application
   - Activez **MESSAGE CONTENT INTENT**
   - Copiez le token dans `.env`
   - Invitez le bot sur votre serveur

6. Obtenez votre clé API :
   - OpenAI : [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Claude : [console.anthropic.com](https://console.anthropic.com)

## 🎮 Utilisation

### Démarrer le bot

```bash
python main.py
```

### Commandes disponibles

- `/mode1` ou `/branding` - Active le mode Client Branding/Web/Graphisme
- `/mode2` ou `/gamemaster` - Active le mode Maître du Jeu
- `/mode3` ou `/webradio` - Active le mode Partenaire Webradio
- `/mode4` ou `/organisation` - Active le mode Client Organisation
- `/help` - Affiche l'aide et les commandes disponibles
- `/reset` - Réinitialise la conversation et revient au mode par défaut

## 💡 Conseils d'utilisation

- Posez des questions pour comprendre les vrais besoins du client
- Écoutez les objections et répondez avec des preuves concrètes
- Proposez de la valeur, pas juste un prix
- Restez professionnel même face à un client difficile
- Utilisez `/reset` pour recommencer un exercice

## 📁 Structure du projet

```
discord-sales-bot/
├── src/
│   ├── commands/        # Commandes Discord
│   ├── modes/           # Modes de clients
│   ├── prompts/         # Prompts RCT (Rôle, Contexte, Tâche)
│   └── utils/           # Utilitaires (API IA, sessions)
├── tests/               # Tests unitaires
├── main.py              # Point d'entrée
├── requirements.txt     # Dépendances Python
└── .env.example         # Template de configuration
```

## 🔧 Configuration avancée

### Modèles IA supportés

- **OpenAI** : GPT-4, GPT-3.5-turbo
- **Claude** : Claude 3 Opus, Claude 3 Sonnet (à configurer)

### Variables d'environnement

Consultez `.env.example` pour la liste complète des variables configurables.

## 📝 Développement

### Contribuer

Les contributions sont les bienvenues ! Consultez `PLAN_DEV_BOT_DISCORD.md` pour le plan de développement complet.

### Tests

```bash
pytest tests/
```

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

Inspiré par les meilleures pratiques de [chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

**Bon courage pour vos entraînements de vente ! 🚀**
