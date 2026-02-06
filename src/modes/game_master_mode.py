"""
Game Master mode for RPG illustration sales.
"""
from typing import Optional
from .base_mode import BaseMode


class GameMasterMode(BaseMode):
    """
    Game Master persona: experienced, cultured, demanding TTRPG player
    skeptical of AI-generated art.
    """

    def __init__(self):
        """Initialize Game Master mode."""
        super().__init__("game_master.md")

    def get_mode_name(self) -> str:
        """Get the display name of this mode."""
        return "Game Master JDR"

    def get_initial_message(self) -> Optional[str]:
        """
        Game Master mode waits for the user to pitch their RPG illustrations.

        Returns:
            None - waits for user input
        """
        return None
