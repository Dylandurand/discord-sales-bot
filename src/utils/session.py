"""
Gestion des sessions utilisateur
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, TYPE_CHECKING
import os

if TYPE_CHECKING:
    from ..modes.base_mode import BaseMode


class UserSession:
    """Représente une session utilisateur avec son historique de conversation"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_mode: Optional['BaseMode'] = None  # Mode actif (instance de BaseMode)
        self.conversation_history: List[Dict[str, str]] = []
        self.started_at = datetime.now()
        self.last_activity = datetime.now()
        
    def add_message(self, role: str, content: str):
        """Ajoute un message à l'historique"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        self.last_activity = datetime.now()
        
        # Limiter l'historique selon MAX_CONVERSATION_HISTORY
        max_history = int(os.getenv('MAX_CONVERSATION_HISTORY', 20))
        if len(self.conversation_history) > max_history:
            # Garder le premier message système et les N derniers messages
            system_messages = [msg for msg in self.conversation_history if msg['role'] == 'system']
            user_messages = [msg for msg in self.conversation_history if msg['role'] != 'system']
            
            # Garder seulement les derniers messages
            keep_count = max_history - len(system_messages)
            self.conversation_history = system_messages + user_messages[-keep_count:]
    
    def set_mode(self, mode: Optional['BaseMode']):
        """
        Change le mode actif.

        Args:
            mode: Instance de BaseMode ou None pour désactiver le mode
        """
        self.current_mode = mode
        
    def reset(self):
        """Réinitialise la session"""
        self.current_mode = None
        self.conversation_history = []
        self.started_at = datetime.now()
        self.last_activity = datetime.now()
        
    def is_expired(self) -> bool:
        """Vérifie si la session a expiré"""
        timeout_minutes = int(os.getenv('SESSION_TIMEOUT_MINUTES', 60))
        timeout = timedelta(minutes=timeout_minutes)
        return datetime.now() - self.last_activity > timeout
        
    def get_history(self) -> List[Dict[str, str]]:
        """Retourne l'historique de conversation"""
        return self.conversation_history.copy()


class SessionManager:
    """Gestionnaire de sessions utilisateur"""
    
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}
        
    def get_session(self, user_id: int) -> UserSession:
        """Récupère ou crée une session utilisateur"""
        # Créer une nouvelle session si elle n'existe pas
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id)
        
        session = self.sessions[user_id]
        
        # Réinitialiser si expirée
        if session.is_expired():
            session.reset()
            
        return session
        
    def reset_session(self, user_id: int):
        """Réinitialise une session utilisateur"""
        if user_id in self.sessions:
            self.sessions[user_id].reset()
        
    def cleanup_expired_sessions(self):
        """Nettoie les sessions expirées (pour optimisation mémoire)"""
        expired_users = [
            user_id for user_id, session in self.sessions.items()
            if session.is_expired()
        ]
        for user_id in expired_users:
            del self.sessions[user_id]
            
    def get_active_sessions_count(self) -> int:
        """Retourne le nombre de sessions actives"""
        return len([s for s in self.sessions.values() if not s.is_expired()])
