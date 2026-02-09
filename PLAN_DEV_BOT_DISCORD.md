# Plan de Développement - Bot Discord Challenge Commercial

## Vue d'ensemble du projet

Bot Discord d'entraînement commercial avec 4 modes de clients différents pour pratiquer la vente de solutions créatives et organisationnelles.

---

## Phase 1 : Configuration de l'environnement ✅

### 1.1 Prérequis système ✅
- [x] Vérifier Python 3.9+ installé (Python 3.12.3 ✓)
- [x] Installer les dépendances de base (`discord.py`, `python-dotenv`, `openai` ou `anthropic`)
- [x] Créer la structure du projet

### 1.2 Configuration Discord ⬜
- [x] Créer une application sur [Discord Developer Portal](https://discord.com/developers/applications)
- [x] Créer le bot dans l'application
- [x] Récupérer le token du bot
- [x] Activer MESSAGE CONTENT INTENT dans les paramètres
- [x] Générer l'URL d'invitation OAuth2 avec les permissions nécessaires
- [x] Inviter le bot sur un serveur de test

### 1.3 Configuration API IA ✅
- [x] Choisir le fournisseur IA (OpenAI GPT-4, Claude, ou autre)
- [x] Obtenir la clé API
- [x] Créer le fichier `.env` avec les tokens
- [x] Créer `.env.example` comme modèle

**Fichiers à créer :**
- `requirements.txt`
- `.env`
- `.env.example`
- `.gitignore`

---

## Phase 2 : Architecture de base ✅

### 2.1 Structure du projet ✅
```
discord-sales-bot/
├── src/
│   ├── __init__.py
│   ├── bot.py              # Point d'entrée principal
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── modes.py        # Commandes de mode
│   │   ├── help.py         # Commande /help
│   │   └── reset.py        # Commande /reset
│   ├── modes/
│   │   ├── __init__.py
│   │   ├── base_mode.py    # Classe abstraite
│   │   ├── branding.py     # Mode 1
│   │   ├── game_master.py  # Mode 2
│   │   ├── webradio.py     # Mode 3
│   │   └── organization.py # Mode 4
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── system_base.txt # Prompt système de base
│   │   ├── mode1_branding.txt
│   │   ├── mode2_gamemaster.txt
│   │   ├── mode3_webradio.txt
│   │   └── mode4_organization.txt
│   └── utils/
│       ├── __init__.py
│       ├── ai_client.py    # Client API IA
│       └── session.py      # Gestion des sessions utilisateur
├── tests/
│   └── __init__.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

### 2.2 Fichiers de base ✅
- [x] Créer `main.py` (point d'entrée)
- [x] Créer `src/bot.py` (initialisation du bot Discord)
- [x] Créer `src/utils/ai_client.py` (wrapper API IA)
- [x] Créer `src/utils/session.py` (gestion état utilisateur)

---

## Phase 3 : Système de modes ⬜

### 3.1 Classe abstraite BaseMode ⬜
- [ ] Créer `src/modes/base_mode.py`
- [ ] Définir l'interface commune pour tous les modes
- [ ] Implémenter la logique de gestion de prompts système
- [ ] Méthode `get_system_prompt()` pour charger le prompt RCT
- [ ] Méthode `handle_message()` pour traiter les messages

### 3.2 Implémentation des 4 modes ⬜

#### Mode 1 : Client Branding/Web/Graphisme ⬜
- [ ] Créer `src/modes/branding.py`
- [ ] Créer le prompt RCT dans `src/prompts/mode1_branding.txt`
- [ ] Définir la personnalité : client pénible, exigeant sur le ROI
- [ ] Implémenter les objections typiques (prix, délais, portfolio)
- [ ] Tester les scénarios de vente

**Caractéristiques du client :**
- Sceptique sur la valeur du design
- Veut des preuves concrètes (études de cas, métriques)
- Budget serré mais exigences élevées
- Comparaison constante avec la concurrence

#### Mode 2 : Maître du Jeu (Game Master) ⬜
- [ ] Créer `src/modes/game_master.py`
- [ ] Créer le prompt RCT dans `src/prompts/mode2_gamemaster.txt`
- [ ] Définir la personnalité : passionné mais exigeant sur la cohérence
- [ ] Implémenter les objections typiques (style artistique, cohérence, droits)
- [ ] Tester les scénarios de vente

**Caractéristiques du client :**
- Très précis sur l'univers et le style
- Veut des personnages avec du background
- Budget limité mais projet de passion
- Nécessite plusieurs révisions

#### Mode 3 : Partenaire Webradio ⬜
- [ ] Créer `src/modes/webradio.py`
- [ ] Créer le prompt RCT dans `src/prompts/mode3_webradio.txt`
- [ ] Définir la personnalité : business-oriented, veut du ROI mesurable
- [ ] Implémenter les objections typiques (audience, analytics, tarifs)
- [ ] Tester les scénarios de vente

**Caractéristiques du client :**
- Veut des statistiques d'audience précises
- Compare avec d'autres canaux publicitaires
- Négocie les tarifs agressivement
- Veut des garanties de résultats

#### Mode 4 : Client Organisation/Productivité ⬜
- [ ] Créer `src/modes/organization.py`
- [ ] Créer le prompt RCT dans `src/prompts/mode4_organization.txt`
- [ ] Définir la personnalité : débordé, sceptique sur les nouvelles méthodes
- [ ] Implémenter les objections typiques (complexité, temps d'apprentissage)
- [ ] Tester les scénarios de vente

**Caractéristiques du client :**
- A déjà essayé plusieurs solutions sans succès
- Manque de temps pour apprendre un nouvel outil
- Veut quelque chose de simple et immédiatement efficace
- Crainte du changement

---

## Phase 4 : Système de commandes slash ⬜

### 4.1 Commandes de mode ⬜
- [ ] Implémenter `/mode1` ou `/branding` - Active le mode Client Branding
- [ ] Implémenter `/mode2` ou `/gamemaster` - Active le mode Maître du Jeu
- [ ] Implémenter `/mode3` ou `/webradio` - Active le mode Partenaire Webradio
- [ ] Implémenter `/mode4` ou `/organisation` - Active le mode Client Organisation
- [ ] Ajouter des confirmations visuelles (embeds Discord)
- [ ] Afficher une description du mode activé

### 4.2 Commande /help ⬜
- [ ] Créer `src/commands/help.py`
- [ ] Lister toutes les commandes disponibles
- [ ] Expliquer le fonctionnement de chaque mode
- [ ] Ajouter des tips pour améliorer ses compétences de vente
- [ ] Format : Embed Discord avec couleurs et emojis

**Contenu de /help :**
```
🎯 BOT DISCORD CHALLENGE COMMERCIAL

Ce bot vous permet de vous entraîner à vendre vos services face à des clients difficiles.

📋 COMMANDES DISPONIBLES :
/mode1 ou /branding - Client cherchant des services de branding/web/graphisme
/mode2 ou /gamemaster - Maître du jeu cherchant des illustrations
/mode3 ou /webradio - Partenaire commercial pour publicité webradio
/mode4 ou /organisation - Client avec problèmes d'organisation

/help - Affiche ce message
/reset - Réinitialise la conversation et revient au mode par défaut

💡 CONSEILS :
- Posez des questions pour comprendre les vrais besoins
- Écoutez les objections et répondez avec des preuves
- Proposez de la valeur, pas juste un prix
- Restez professionnel même face à un client difficile

Bon courage ! 🚀
```

### 4.3 Commande /reset ⬜
- [ ] Créer `src/commands/reset.py`
- [ ] Effacer l'historique de conversation de l'utilisateur
- [ ] Revenir au mode par défaut (client pénible générique)
- [ ] Confirmer la réinitialisation à l'utilisateur
- [ ] Permettre de recommencer un exercice

---

## Phase 5 : Prompts RCT (Rôle, Contexte, Tâche) ⬜

### 5.1 Structure des prompts ⬜
- [ ] Créer le template de base pour tous les prompts
- [ ] Définir le comportement "client pénible" de base
- [ ] Intégrer les spécificités de chaque mode

**Template RCT :**
```
# RÔLE
Tu es [description du client selon le mode]...

# CONTEXTE
L'utilisateur est un professionnel qui souhaite te vendre ses services...
Tu dois être exigeant, poser des questions difficiles, et ne pas céder facilement...

# COMPORTEMENT DE BASE
- Tu es proche de ton argent et méfiant
- Tu veux des preuves concrètes de la valeur
- Tu compares avec la concurrence
- Tu poses des questions pièges
- Tu n'acceptes que si tu vois un vrai bénéfice

# TÂCHE
Joue le rôle de ce client difficile. Commence par...
```

### 5.2 Rédaction des prompts spécifiques ⬜
- [ ] Rédiger `mode1_branding.txt` (à faire plus tard selon vos instructions)
- [ ] Rédiger `mode2_gamemaster.txt` (à faire plus tard selon vos instructions)
- [ ] Rédiger `mode3_webradio.txt` (à faire plus tard selon vos instructions)
- [ ] Rédiger `mode4_organization.txt` (à faire plus tard selon vos instructions)
- [ ] Rédiger `system_base.txt` (comportement par défaut)

---

## Phase 6 : Gestion des sessions utilisateur ⬜

### 6.1 Système de sessions ⬜
- [ ] Créer la classe `SessionManager` dans `src/utils/session.py`
- [ ] Stocker l'état de chaque utilisateur (mode actif, historique)
- [ ] Implémenter la persistance temporaire en mémoire
- [ ] Gérer le timeout des sessions (optionnel)
- [ ] Permettre plusieurs utilisateurs simultanés

**Données par session :**
- `user_id` : ID Discord de l'utilisateur
- `current_mode` : Mode actif (1-4 ou défaut)
- `conversation_history` : Liste des messages
- `started_at` : Timestamp de début
- `last_activity` : Timestamp dernière activité

### 6.2 Gestion de l'historique ⬜
- [ ] Limiter l'historique à X messages (ex: 20 derniers)
- [ ] Implémenter la fonction de reset
- [ ] Conserver le contexte entre les messages
- [ ] Optimiser les tokens envoyés à l'API IA

---

## Phase 7 : Intégration API IA ⬜

### 7.1 Client API IA ⬜
- [ ] Créer la classe `AIClient` dans `src/utils/ai_client.py`
- [ ] Supporter OpenAI GPT-4 / GPT-3.5-turbo
- [ ] Supporter Claude (optionnel)
- [ ] Gérer les erreurs API (rate limit, timeout, etc.)
- [ ] Implémenter des retry automatiques
- [ ] Logger les appels pour debug

### 7.2 Optimisation des coûts ⬜
- [ ] Limiter la longueur des messages
- [ ] Compresser l'historique si nécessaire
- [ ] Utiliser GPT-3.5-turbo pour les tests
- [ ] Implémenter un système de cache si pertinent

---

## Phase 8 : Interface utilisateur Discord ⬜

### 8.1 Messages et embeds ⬜
- [ ] Créer des embeds visuels pour les changements de mode
- [ ] Ajouter des emojis pour rendre le bot plus engageant
- [ ] Différencier visuellement chaque mode (couleurs)
- [ ] Ajouter un footer avec des infos utiles

**Couleurs par mode :**
- Mode 1 (Branding) : Bleu (#3498db)
- Mode 2 (Game Master) : Violet (#9b59b6)
- Mode 3 (Webradio) : Orange (#e67e22)
- Mode 4 (Organisation) : Vert (#2ecc71)
- Défaut/Reset : Gris (#95a5a6)

### 8.2 Gestion des erreurs utilisateur ⬜
- [ ] Détecter les commandes invalides
- [ ] Messages d'erreur clairs et utiles
- [ ] Rediriger vers /help si confusion
- [ ] Gérer les messages trop longs

---

## Phase 9 : Tests et validation ⬜

### 9.1 Tests unitaires ⬜
- [ ] Tester la classe `SessionManager`
- [ ] Tester le chargement des prompts
- [ ] Tester les commandes slash
- [ ] Tester la gestion des erreurs

### 9.2 Tests d'intégration ⬜
- [ ] Tester chaque mode de bout en bout
- [ ] Tester les transitions entre modes
- [ ] Tester /reset et /help
- [ ] Tester avec plusieurs utilisateurs simultanés

### 9.3 Tests utilisateur ⬜
- [ ] Faire des simulations de vente dans chaque mode
- [ ] Vérifier que le client est suffisamment "pénible"
- [ ] Ajuster les prompts selon les retours
- [ ] Valider la qualité des réponses IA

---

## Phase 10 : Documentation et déploiement ⬜

### 10.1 Documentation ⬜
- [ ] Rédiger le `README.md` complet
- [ ] Documenter l'installation et la configuration
- [ ] Ajouter des exemples de conversations
- [ ] Créer un guide d'utilisation

### 10.2 Déploiement ⬜
- [ ] Choisir la plateforme d'hébergement (VPS, Railway, Heroku, etc.)
- [ ] Configurer les variables d'environnement
- [ ] Tester en production
- [ ] Mettre en place le monitoring (logs, uptime)

### 10.3 Maintenance ⬜
- [ ] Créer un système de logging
- [ ] Monitorer les coûts API
- [ ] Planifier les mises à jour des prompts
- [ ] Collecter les feedbacks pour amélioration

---

## Phase 11 : Améliorations futures (optionnel) ⬜

### 11.1 Fonctionnalités avancées ⬜
- [ ] Système de scoring (évaluation de la performance de vente)
- [ ] Statistiques par utilisateur (nombre de sessions, taux de conversion simulé)
- [ ] Mode "formation" avec tips après chaque session
- [ ] Enregistrement des meilleures conversations
- [ ] Partage des scores sur un leaderboard

### 11.2 Modes additionnels ⬜
- [ ] Mode 5 : Client e-commerce
- [ ] Mode 6 : Startup tech
- [ ] Mode 7 : Client corporate
- [ ] Mode personnalisé (l'utilisateur définit son propre client)

### 11.3 Intégrations ⬜
- [ ] Base de données persistante (PostgreSQL/MongoDB)
- [ ] API REST pour statistiques
- [ ] Dashboard web pour suivre la progression
- [ ] Export des conversations en PDF

---

## Checklist de validation finale ⬜

- [ ] Toutes les commandes slash fonctionnent
- [ ] Les 4 modes sont opérationnels et distincts
- [ ] /help affiche les bonnes informations
- [ ] /reset nettoie correctement les sessions
- [ ] Le bot répond de manière cohérente et "pénible"
- [ ] Pas d'erreurs ou de crashs lors de l'utilisation normale
- [ ] Le code est documenté et maintenable
- [ ] Les prompts RCT sont bien structurés
- [ ] Le bot est déployé et accessible 24/7
- [ ] La documentation est complète

---

## Notes importantes

### Sécurité
- Ne jamais commit les fichiers `.env` avec les tokens
- Utiliser des variables d'environnement en production
- Limiter les permissions du bot Discord au strict nécessaire

### Performance
- Implémenter un rate limiting par utilisateur si nécessaire
- Optimiser les appels API pour réduire les coûts
- Mettre en cache les réponses fréquentes si pertinent

### Expérience utilisateur
- Les réponses doivent être rapides (< 5 secondes idéalement)
- Le bot doit être cohérent dans son personnage
- Les transitions entre modes doivent être claires
- Le feedback doit être immédiat

---

## Ressources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Repository de référence](https://github.com/Zero6992/chatGPT-discord-bot)

---

**Date de création :** 2026-02-05
**Version :** 1.0
**Statut :** Prêt pour l'implémentation

---

## Progression globale

```
Phase 1  : ⬜⬜⬜ Configuration environnement (0/3)
Phase 2  : ⬜⬜ Architecture de base (0/2)
Phase 3  : ⬜⬜ Système de modes (0/2)
Phase 4  : ⬜⬜⬜ Commandes slash (0/3)
Phase 5  : ⬜⬜ Prompts RCT (0/2)
Phase 6  : ⬜⬜ Sessions utilisateur (0/2)
Phase 7  : ⬜⬜ Intégration API IA (0/2)
Phase 8  : ⬜⬜ Interface Discord (0/2)
Phase 9  : ⬜⬜⬜ Tests (0/3)
Phase 10 : ⬜⬜⬜ Déploiement (0/3)

Total : 0/26 sections complétées
```

---

**Prêt à commencer l'implémentation ! 🚀**
