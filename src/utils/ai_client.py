"""
Client API OpenAI - Wrapper pour ChatGPT
"""
import os
from typing import List, Dict
from openai import OpenAI


class AIClient:
    """Client pour l'API OpenAI (ChatGPT)"""
    
    def __init__(self):
        """Initialise le client OpenAI"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY non définie dans .env")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 0.8
    ) -> str:
        """
        Génère une réponse à partir de l'historique de messages
        
        Args:
            messages: Liste de messages au format [{"role": "...", "content": "..."}]
            max_tokens: Nombre maximum de tokens dans la réponse
            temperature: Créativité de la réponse (0.0 à 1.0)
            
        Returns:
            La réponse générée par ChatGPT
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Erreur lors de la génération de réponse : {e}")
            raise
    
    def get_model_info(self) -> Dict[str, str]:
        """Retourne les informations sur le modèle configuré"""
        return {
            "provider": "openai",
            "model": self.model
        }
