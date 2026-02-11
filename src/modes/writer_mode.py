"""
Writer mode for book publishing/buying simulation with persona selection.
"""
from typing import Optional, Dict
from .base_mode import BaseMode


class WriterMode(BaseMode):
    """
    Writer mode with 3 personas:
    - Mireille: LA GARDIENNE DU FANTASTIQUE (Fantasy YA editor)
    - Damien: L'ARCHITECTE DU SUSPENSE (Thriller YA editor)
    - Rémi: L'ACHETEUR SCEPTIQUE (Sceptical book buyer)
    """

    PERSONAS = {
        "mireille": {
            "name": "Mireille - LA GARDIENNE DU FANTASTIQUE",
            "prompt_file": "ecriture_fantasy.md",
            "description": "Éditrice senior YA fantastique, exigeante sur la voix et le positionnement éditorial",
            "emoji": "✨"
        },
        "damien": {
            "name": "Damien - L'ARCHITECTE DU SUSPENSE",
            "prompt_file": "ecriture_thriller.md",
            "description": "Éditeur senior thriller YA, rigoureux sur la logique, le rythme et la crédibilité",
            "emoji": "🔪"
        },
        "remi": {
            "name": "Rémi - L'ACHETEUR SCEPTIQUE",
            "prompt_file": "acheteur_roman_thriller_fantasy.md",
            "description": "Acheteur YA sceptique, compare tout aux écrans et remet en cause le format papier",
            "emoji": "😤"
        }
    }

    def __init__(self, persona_key: Optional[str] = None):
        """
        Initialize Writer mode with optional persona.

        Args:
            persona_key: Key of the persona ("mireille", "damien", or "remi").
                        If None, no persona is selected yet.
        """
        self.persona_key = persona_key
        self.persona_selected = persona_key is not None

        if self.persona_selected:
            if persona_key not in self.PERSONAS:
                raise ValueError(f"Unknown persona: {persona_key}")
            prompt_file = self.PERSONAS[persona_key]["prompt_file"]
        else:
            # Temporary prompt until persona is selected
            prompt_file = "ecriture_fantasy.md"  # Default, will be replaced

        super().__init__(prompt_file)

    def set_persona(self, persona_key: str) -> None:
        """
        Set the persona for this writer session.

        Args:
            persona_key: Key of the persona ("mireille", "damien", or "remi")

        Raises:
            ValueError: If persona_key is not valid
        """
        if persona_key not in self.PERSONAS:
            raise ValueError(f"Unknown persona: {persona_key}")

        self.persona_key = persona_key
        self.persona_selected = True
        self.prompt_file = self.PERSONAS[persona_key]["prompt_file"]
        self.system_prompt = self._load_prompt()
        self.reset_score()

    def get_mode_name(self) -> str:
        """Get the display name including persona if selected."""
        if self.persona_selected:
            return f"Écriture - {self.PERSONAS[self.persona_key]['name']}"
        return "Écriture (Sélection de persona)"

    def get_initial_message(self) -> Optional[str]:
        """
        Get the initial message.
        If no persona selected, show selection menu.
        If persona selected, return None to wait for user's pitch.
        """
        if not self.persona_selected:
            return self._get_persona_selection_menu()
        return None

    def _get_persona_selection_menu(self) -> str:
        """
        Generate the persona selection menu.

        Returns:
            Formatted menu message
        """
        menu = "# ✍️ Mode Écriture - Sélection de Persona\n\n"
        menu += "Choisissez votre interlocuteur éditorial :\n\n"

        for key, persona in self.PERSONAS.items():
            menu += f"**{persona['emoji']} {key.upper()}** - {persona['name']}\n"
            menu += f"_{persona['description']}_\n\n"

        menu += "\n📝 **Pour sélectionner un persona, tapez son nom** : `mireille`, `damien` ou `remi`"

        return menu

    @staticmethod
    def get_persona_selection_message() -> str:
        """
        Static method to get the persona selection menu.
        Used when starting /ecriture command.

        Returns:
            Formatted menu message
        """
        menu = "# ✍️ Mode Écriture - Sélection de Persona\n\n"
        menu += "Choisissez votre interlocuteur éditorial :\n\n"

        for key, persona in WriterMode.PERSONAS.items():
            menu += f"**{persona['emoji']} {key.upper()}** - {persona['name']}\n"
            menu += f"_{persona['description']}_\n\n"

        menu += "\n📝 **Pour sélectionner un persona, tapez son nom** : `mireille`, `damien` ou `remi`"

        return menu

    @staticmethod
    def is_valid_persona(text: str) -> bool:
        """
        Check if text is a valid persona selection.

        Args:
            text: User input text

        Returns:
            True if text matches a persona key
        """
        return text.lower().strip() in WriterMode.PERSONAS.keys()

    @staticmethod
    def get_persona_key(text: str) -> Optional[str]:
        """
        Extract persona key from user text.

        Args:
            text: User input text

        Returns:
            Persona key if valid, None otherwise
        """
        cleaned = text.lower().strip()
        if cleaned in WriterMode.PERSONAS.keys():
            return cleaned
        return None
