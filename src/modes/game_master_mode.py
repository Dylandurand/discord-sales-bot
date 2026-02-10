"""
Game Master mode for RPG illustration sales with persona selection.
"""
from typing import Optional, Dict
from .base_mode import BaseMode


class GameMasterMode(BaseMode):
    """
    Game Master mode with 2 personas:
    - Gaël: LE MAÎTRE EXIGEANT
    - Lyra: LA BÂTISSEUSE D'UNIVERS
    """

    PERSONAS = {
        "gael": {
            "name": "Gaël - LE MAÎTRE EXIGEANT",
            "prompt_file": "game_master.md",
            "description": "MJ expérimenté, cherche immersion et valeur narrative concrète",
            "emoji": "🎲"
        },
        "lyra": {
            "name": "Lyra - LA BÂTISSEUSE D'UNIVERS",
            "prompt_file": "game_master_worldbuilder.md",
            "description": "Worldbuilder narratif, cherche cohérence du lore et outils multi-sensoriels",
            "emoji": "🌍"
        },
        "sylvan": {
            "name": "Sylvan - LE GARDIEN DU VIVANT",
            "prompt_file": "game_master_conservation.md",
            "description": "World Builder conservation, ancre les créatures dans le vivant menacé",
            "emoji": "🌿"
        }
    }

    def __init__(self, persona_key: Optional[str] = None):
        """
        Initialize Game Master mode with optional persona.

        Args:
            persona_key: Key of the persona ("gael" or "lyra").
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
            prompt_file = "game_master.md"  # Default, will be replaced

        super().__init__(prompt_file)

    def set_persona(self, persona_key: str) -> None:
        """
        Set the persona for this game master session.

        Args:
            persona_key: Key of the persona ("gael" or "lyra")

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
            return f"Game Master - {self.PERSONAS[self.persona_key]['name']}"
        return "Game Master (Sélection de persona)"

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
        menu = "# 🎲 Mode Game Master - Sélection de Persona\n\n"
        menu += "Choisissez votre profil de Maître de Jeu :\n\n"

        for key, persona in self.PERSONAS.items():
            menu += f"**{persona['emoji']} {key.upper()}** - {persona['name']}\n"
            menu += f"_{persona['description']}_\n\n"

        menu += "\n📝 **Pour sélectionner un persona, tapez son nom** : `gael`, `lyra` ou `sylvan`"

        return menu

    @staticmethod
    def get_persona_selection_message() -> str:
        """
        Static method to get the persona selection menu.
        Used when starting /game_master command.

        Returns:
            Formatted menu message
        """
        menu = "# 🎲 Mode Game Master - Sélection de Persona\n\n"
        menu += "Choisissez votre profil de Maître de Jeu :\n\n"

        for key, persona in GameMasterMode.PERSONAS.items():
            menu += f"**{persona['emoji']} {key.upper()}** - {persona['name']}\n"
            menu += f"_{persona['description']}_\n\n"

        menu += "\n📝 **Pour sélectionner un persona, tapez son nom** : `gael`, `lyra` ou `sylvan`"

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
        return text.lower().strip() in GameMasterMode.PERSONAS.keys()

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
        if cleaned in GameMasterMode.PERSONAS.keys():
            return cleaned
        return None
