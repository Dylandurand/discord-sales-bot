"""
Branding mode with persona selection.
"""
from typing import Optional, Dict
from .base_mode import BaseMode


class BrandingMode(BaseMode):
    """
    Branding mode with 3 personas:
    - Clara: L'ÉQUILIBRISTE ÉPUISÉ·E
    - Antoine: LE STRATÈGE LUCIDE
    - Julie: LE SCEPTIQUE DOMINANT
    """

    PERSONAS = {
        "clara": {
            "name": "Clara - L'ÉQUILIBRISTE ÉPUISÉ·E",
            "prompt_file": "branding_clara.md",
            "description": "Créatif·ve épuisé·e, cherche simplicité et accompagnement",
            "emoji": "🌸"
        },
        "antoine": {
            "name": "Antoine - LE STRATÈGE LUCIDE",
            "prompt_file": "branding_antoine.md",
            "description": "Entrepreneur expérimenté, cherche vision et ROI clair",
            "emoji": "🎯"
        },
        "julie": {
            "name": "Julie - LE SCEPTIQUE DOMINANT",
            "prompt_file": "branding_julie.md",
            "description": "Client dominant et pressé, teste l'autorité du prestataire",
            "emoji": "⚡"
        }
    }

    def __init__(self, persona_key: Optional[str] = None):
        """
        Initialize Branding mode with optional persona.

        Args:
            persona_key: Key of the persona ("clara", "antoine", or "julie").
                        If None, no persona is selected yet.
        """
        self.persona_key = persona_key
        self.persona_selected = persona_key is not None

        if self.persona_selected:
            if persona_key not in self.PERSONAS:
                raise ValueError(f"Unknown persona: {persona_key}")
            prompt_file = self.PERSONAS[persona_key]["prompt_file"]
        else:
            # Temporary empty prompt until persona is selected
            prompt_file = "branding_clara.md"  # Default, will be replaced

        super().__init__(prompt_file)

    def set_persona(self, persona_key: str) -> None:
        """
        Set the persona for this branding session.

        Args:
            persona_key: Key of the persona ("clara", "antoine", or "julie")

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
            return f"Branding - {self.PERSONAS[self.persona_key]['name']}"
        return "Branding (Sélection de persona)"

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
        menu = "# 🎭 Mode Branding - Sélection de Persona\n\n"
        menu += "Choisissez votre client pénible :\n\n"

        for key, persona in self.PERSONAS.items():
            menu += f"**{persona['emoji']} {key.upper()}** - {persona['name']}\n"
            menu += f"_{persona['description']}_\n\n"

        menu += "\n📝 **Pour sélectionner un persona, tapez son nom** : `clara`, `antoine`, ou `julie`"

        return menu

    @staticmethod
    def get_persona_selection_message() -> str:
        """
        Static method to get the persona selection menu.
        Used when starting /branding command.

        Returns:
            Formatted menu message
        """
        menu = "# 🎭 Mode Branding - Sélection de Persona\n\n"
        menu += "Choisissez votre client pénible :\n\n"

        for key, persona in BrandingMode.PERSONAS.items():
            menu += f"**{persona['emoji']} {key.upper()}** - {persona['name']}\n"
            menu += f"_{persona['description']}_\n\n"

        menu += "\n📝 **Pour sélectionner un persona, tapez son nom** : `clara`, `antoine`, ou `julie`"

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
        return text.lower().strip() in BrandingMode.PERSONAS.keys()

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
        if cleaned in BrandingMode.PERSONAS.keys():
            return cleaned
        return None
