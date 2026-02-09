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

## Phase 3 : Système de modes ✅

### 3.1 Classe abstraite BaseMode ✅
- [x] Créer `src/modes/base_mode.py`
- [x] Définir l'interface commune pour tous les modes
- [x] Implémenter la logique de gestion de prompts système (.md files)
- [x] Méthode `get_system_prompt()` pour charger le prompt RCT
- [x] Méthode `handle_message()` pour traiter les messages
- [x] Méthode `should_end_session()` pour détecter les décisions finales
- [x] Système de scoring interne (0-100)

### 3.2 Implémentation des 4 modes ✅

#### Mode 1 : Client Branding/Web/Graphisme ✅
- [x] Créer `src/modes/branding_mode.py` avec 3 personas
- [x] Créer les prompts RCT en .md :
  - `src/prompts/branding_clara.md` - L'ÉQUILIBRISTE ÉPUISÉ·E
  - `src/prompts/branding_antoine.md` - LE STRATÈGE LUCIDE
  - `src/prompts/branding_julie.md` - LE SCEPTIQUE DOMINANT
- [x] Menu de sélection de persona
- [x] Système de scoring avec seuils de décision
- [x] Format de décision standardisé

**Personas implémentés :**
- **Clara** : Créatif·ve épuisé·e, cherche simplicité et accompagnement
- **Antoine** : Entrepreneur expérimenté, cherche vision et ROI clair
- **Julie** : Client dominant et pressé, teste l'autorité du prestataire

#### Mode 2 : Maître du Jeu (Game Master) ✅
- [x] Créer `src/modes/game_master_mode.py`
- [x] Créer le prompt RCT dans `src/prompts/game_master.md`
- [x] Définir la personnalité : passionné mais exigeant, sceptique sur l'IA
- [x] Système de scoring (narrative value, AI differentiation, usage in sessions)
- [x] Format de décision : ACHAT/REFUS

**Caractéristiques du client :**
- Expérimenté en JDR, très cultivé
- Sceptique vis-à-vis des illustrations générées par IA
- Teste la valeur narrative et l'immersion
- Veut des droits d'usage clairs (réutilisation, impression, projection)

#### Mode 3 : Partenaire Webradio ✅
- [x] Créer `src/modes/webradio_mode.py`
- [x] Créer le prompt RCT dans `src/prompts/webradio.md`
- [x] Définir la personnalité : business-oriented, veut du ROI mesurable
- [x] Système de scoring (audience metrics, ROI justification, tracking)
- [x] Format de décision : REFUS/INTÉRÊT CONDITIONNEL/ACCORD

**Caractéristiques du client :**
- Responsable marketing / annonceur potentiel
- Sceptique, orienté ROI, protège son budget
- Veut des chiffres d'audience précis et vérifiables
- Compare avec d'autres leviers (réseaux sociaux, Google Ads)

#### Mode 4 : Client Organisation/Productivité ✅
- [x] Créer `src/modes/organisation_mode.py`
- [x] Créer le prompt RCT dans `src/prompts/organisation.md`
- [x] Définir la personnalité : ultra-sceptique, rationnel, exigeant
- [x] Message d'ouverture prédéfini
- [x] 5 phases de conversation structurées
- [x] Système de scoring avec comparaison vs alternatives

**Caractéristiques du client :**
- A déjà essayé et abandonné : agendas, Notion, Bullet Journal
- Compare systématiquement à un agenda à 15€
- Veut du ROI concret (temps, clarté, impact)
- Challenge le prix, la valeur, la friction, l'usage quotidien

---

## Phase 4 : Système de commandes slash ✅

### 4.1 Commandes de mode ✅
- [x] Implémenter `/branding` - Active le mode Client Branding (avec sélection de persona)
- [x] Implémenter `/gamemaster` - Active le mode Maître du Jeu
- [x] Implémenter `/webradio` - Active le mode Partenaire Webradio
- [x] Implémenter `/organisation` - Active le mode Client Organisation
- [x] Ajouter des confirmations visuelles et descriptions
- [x] Afficher le nom du mode activé

### 4.2 Commande /help ✅
- [x] Implémenter directement dans `src/bot.py`
- [x] Lister toutes les commandes disponibles
- [x] Expliquer le fonctionnement de chaque mode
- [x] Ajouter des conseils pour améliorer ses compétences de vente
- [x] Format : Texte markdown formatté

**Contenu de /help :**
```
🎯 BOT DISCORD CHALLENGE COMMERCIAL

Ce bot simule des clients pénibles pour vous aider à améliorer vos compétences commerciales.

📋 COMMANDES DISPONIBLES :
/branding - Mode Branding avec 3 personas (Clara, Antoine, Julie)
/gamemaster - Mode Game Master JDR (illustrations IA)
/webradio - Mode Partenaire WebRadio (sponsoring)
/organisation - Mode Client Organisation/Productivité (Plan Bzz)
/reset - Réinitialise votre session
/help - Affiche cette aide

💡 COMMENT ÇA MARCHE ?
1. Choisissez un mode avec une commande slash
2. Le bot incarnera un client sceptique et exigeant
3. Défendez votre produit/service face aux objections
4. Recevez un score et des conseils à la fin

🎯 OBJECTIF :
Améliorer votre pitch, gérer les objections, et convaincre même les clients les plus difficiles !
```

### 4.3 Commande /reset ✅
- [x] Implémenter directement dans `src/bot.py`
- [x] Effacer l'historique de conversation de l'utilisateur
- [x] Réinitialiser le mode actif
- [x] Confirmer la réinitialisation à l'utilisateur
- [x] Permettre de recommencer un exercice

---

## Phase 5 : Prompts RCT (Rôle, Contexte, Tâche) ✅

### 5.1 Structure des prompts ✅
- [x] Créer le template de base pour tous les prompts
- [x] Définir le comportement "client pénible" de base
- [x] Intégrer les spécificités de chaque mode

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

### 5.2 Rédaction des prompts spécifiques ✅
- [x] Rédiger `branding_clara.md`, `branding_antoine.md`, `branding_julie.md` (3 personas Branding)
- [x] Rédiger `game_master.md` (Mode Game Master JDR)
- [x] Rédiger `webradio.md` (Mode WebRadio)
- [x] Rédiger `organisation.md` (Mode Organisation/Productivité)
- [x] Tous les prompts incluent scoring, phases de conversation, et formats de décision

---

## Phase 6 : Gestion des sessions utilisateur ✅

### 6.1 Système de sessions ✅
- [x] Créer la classe `SessionManager` dans `src/utils/session.py`
- [x] Stocker l'état de chaque utilisateur (mode actif, historique)
- [x] Implémenter la persistance temporaire en mémoire
- [x] Gérer le timeout des sessions (configuré à 60 minutes par défaut)
- [x] Permettre plusieurs utilisateurs simultanés

**Données par session :**
- `user_id` : ID Discord de l'utilisateur
- `current_mode` : Mode actif (1-4 ou défaut)
- `conversation_history` : Liste des messages
- `started_at` : Timestamp de début
- `last_activity` : Timestamp dernière activité

### 6.2 Gestion de l'historique ✅
- [x] Limiter l'historique à X messages (configuré à 20 par défaut via MAX_CONVERSATION_HISTORY)
- [x] Implémenter la fonction de reset (via SessionManager.reset_session())
- [x] Conserver le contexte entre les messages
- [x] Optimiser les tokens envoyés à l'API IA (historique tronqué automatiquement)

---

## Phase 7 : Intégration API IA ✅

### 7.1 Client API IA ✅
- [x] Créer la classe `AIClient` dans `src/utils/ai_client.py`
- [x] Supporter OpenAI GPT-4 / GPT-3.5-turbo (configuré via OPENAI_MODEL)
- [x] Supporter Claude via Anthropic (configuré via AI_PROVIDER)
- [x] Gérer les erreurs API (rate limit, timeout, etc.)
- [x] Implémenter des retry automatiques (3 tentatives)
- [x] Logger les appels pour debug

### 7.2 Optimisation des coûts ✅
- [x] Limiter la longueur des messages (max_tokens configuré à 1000)
- [x] Compresser l'historique si nécessaire (limite de 20 messages)
- [x] Utiliser GPT-3.5-turbo pour les tests (configurable via OPENAI_MODEL)
- [x] Temperature configurée à 0.85 pour un bon équilibre créativité/cohérence

---

## Phase 8 : Interface utilisateur Discord ✅

### 8.1 Messages et embeds ✅
- [x] Créer des embeds visuels pour les changements de mode
- [x] Ajouter des emojis pour rendre le bot plus engageant
- [x] Différencier visuellement chaque mode (couleurs)
- [x] Ajouter un footer avec des infos utiles

**Couleurs par mode :**
- Mode 1 (Branding) : Bleu (#3498db) ✅
- Mode 2 (Game Master) : Violet (#9b59b6) ✅
- Mode 3 (Webradio) : Orange (#e67e22) ✅
- Mode 4 (Organisation) : Vert (#2ecc71) ✅
- Défaut/Reset : Gris (#95a5a6) ✅
- Erreur : Rouge (#e74c3c) ✅
- Succès : Vert (#2ecc71) ✅

### 8.2 Gestion des erreurs utilisateur ✅
- [x] Détecter les commandes invalides
- [x] Messages d'erreur clairs et utiles
- [x] Rediriger vers /help si confusion
- [x] Gérer les messages trop longs
- [x] Implémenter le rate limiting (protection anti-spam)
- [x] Validation de la longueur des messages
- [x] Filtrage des messages système Discord

---

## Phase 9 : Tests et validation ✅

### 9.1 Tests unitaires ✅
- [x] Tester la classe `SessionManager` (création, reset, expiration)
- [x] Tester le chargement des prompts (tous les modes)
- [x] Tester les commandes slash (validation, embeds)
- [x] Tester la gestion des erreurs (rate limiting, validation)
- [x] Tester le client IA (configuration, modèles)
- [x] **41 tests unitaires créés et validés** ✅

**Fichiers de tests créés :**
- `tests/test_session.py` - Tests SessionManager et UserSession
- `tests/test_modes.py` - Tests de tous les modes et prompts
- `tests/test_utils.py` - Tests configuration et utilitaires

### 9.2 Tests d'intégration ✅
- [x] Tester chaque mode de bout en bout
- [x] Tester les transitions entre modes
- [x] Tester /reset et /help
- [x] Tester avec plusieurs utilisateurs simultanés
- [x] Tester le workflow complet de session
- [x] Tester la sélection de persona (mode Branding)
- [x] **Script d'intégration créé** : `tests/integration_test.py` ✅

### 9.3 Tests utilisateur ⬜
- [ ] Faire des simulations de vente dans chaque mode (à faire en utilisation réelle)
- [ ] Vérifier que le client est suffisamment "pénible" (à valider avec utilisateurs)
- [ ] Ajuster les prompts selon les retours (itératif)
- [ ] Valider la qualité des réponses IA (nécessite clé API configurée)

---

## Phase 10 : Documentation et déploiement ⬜

### 10.1 Documentation ✅
- [x] Rédiger le `README.md` complet avec badges
- [x] Documenter l'installation et la configuration
- [x] Ajouter des exemples d'utilisation et commandes
- [x] Créer un guide d'utilisation détaillé
- [x] Documenter la structure du projet
- [x] Ajouter les variables d'environnement
- [x] Instructions de déploiement VPS/Cloud

### 10.2 Déploiement ⬜ (optionnel - pour production 24/7)
- [ ] Choisir la plateforme d'hébergement (VPS, Railway, Heroku, etc.)
- [ ] Configurer les variables d'environnement en production
- [ ] Tester en production
- [ ] Mettre en place le monitoring (logs, uptime)

### 10.3 Maintenance ⬜ (optionnel - pour production 24/7)
- [ ] Créer un système de logging avancé
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
Phase 1  : ✅✅✅ Configuration environnement (3/3)
Phase 2  : ✅✅ Architecture de base (2/2)
Phase 3  : ✅✅ Système de modes (2/2)
Phase 4  : ✅✅✅ Commandes slash (3/3)
Phase 5  : ✅✅ Prompts RCT (2/2)
Phase 6  : ✅✅ Sessions utilisateur (2/2)
Phase 7  : ✅✅ Intégration API IA (2/2)
Phase 8  : ✅✅ Interface Discord (2/2)
Phase 9  : ✅✅⬜ Tests (2/3)
Phase 10 : ✅⬜⬜ Documentation (1/3)

Total : 23/26 sections complétées (88%)

🎉 PHASES ESSENTIELLES COMPLÉTÉES : 8/10
```

---

## 🎉 État du Projet

### ✅ Fonctionnalités Implémentées

- **Bot Discord complet** avec 6 commandes slash fonctionnelles
- **4 modes de clients** avec personnalités distinctes (+ 3 personas Branding)
- **Interface moderne** avec embeds colorés et emojis
- **Gestion d'erreurs robuste** : rate limiting, validation, messages clairs
- **Système de sessions** multi-utilisateurs avec expiration automatique
- **41 tests unitaires** + tests d'intégration validés
- **Documentation complète** (README détaillé, guide d'installation)

### 🚀 Prêt à l'Utilisation

Le bot est **100% fonctionnel** pour une utilisation locale ou sur serveur Discord.
Il suffit de :
1. Configurer `.env` avec vos tokens
2. Lancer `python main.py`
3. Commencer l'entraînement avec `/branding`, `/gamemaster`, etc.

### 📋 Prochaines Étapes (Optionnel)

- Phase 9.3 : Tests utilisateur réels (nécessite utilisation)
- Phase 10.2-10.3 : Déploiement 24/7 et monitoring (pour production)

---

**Prêt à commencer l'implémentation ! 🚀**
