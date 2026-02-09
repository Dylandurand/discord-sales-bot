"""
WebRadio mode for advertising partnerships.
"""
from typing import Optional
from .base_mode import BaseMode


class WebRadioMode(BaseMode):
    """
    WebRadio advertiser persona: skeptical business decision-maker
    focused on ROI and metrics.
    """

    def __init__(self):
        """Initialize WebRadio mode."""
        super().__init__("webradio.md")

    def get_mode_name(self) -> str:
        """Get the display name of this mode."""
        return "Partenaire WebRadio"

    def get_initial_message(self) -> Optional[str]:
        """
        WebRadio mode waits for the user to pitch their radio partnership.

        Returns:
            None - waits for user input
        """
        return None
