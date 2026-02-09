"""
Organisation mode for Plan Bzz agenda-method sales.
"""
from typing import Optional
from .base_mode import BaseMode


class OrganisationMode(BaseMode):
    """
    Organisation/Productivity client persona: ultra-skeptical prospect
    who has tried and abandoned many productivity systems.
    """

    # Predefined opening message from the prompt
    OPENING_MESSAGE = (
        "Ok. J'ai vu passer 200 agendas 'qui changent la vie'. "
        "J'ai déjà testé agenda classique, Notion, et j'ai même tenté le Bullet Journal: "
        "j'abandonne dès que ça devient contraignant.\n\n"
        "Plan Bzz, c'est quoi EN 2 phrases, et en quoi c'est objectivement différent d'un agenda à 15€ ?"
    )

    def __init__(self):
        """Initialize Organisation mode."""
        super().__init__("organisation.md")

    def get_mode_name(self) -> str:
        """Get the display name of this mode."""
        return "Client Organisation/Productivité (Plan Bzz)"

    def get_initial_message(self) -> Optional[str]:
        """
        Organisation mode starts with a predefined skeptical opening.

        Returns:
            The opening challenge message
        """
        return self.OPENING_MESSAGE
