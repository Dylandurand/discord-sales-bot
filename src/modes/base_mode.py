"""
Base mode abstract class for all sales challenge modes.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import os


class BaseMode(ABC):
    """Abstract base class for all bot modes."""

    def __init__(self, prompt_file: str):
        """
        Initialize the mode with its prompt file.

        Args:
            prompt_file: Name of the .md file in src/prompts/ (e.g., "organisation.md")
        """
        self.prompt_file = prompt_file
        self.system_prompt = self._load_prompt()
        self.scoring_enabled = True  # All modes use scoring
        self.current_score = 0  # Internal score tracking (0-100)

    def _load_prompt(self) -> str:
        """
        Load the prompt from the .md file.

        Returns:
            The prompt content as a string.

        Raises:
            FileNotFoundError: If the prompt file doesn't exist.
        """
        # Get the project root directory
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        prompt_path = project_root / "src" / "prompts" / self.prompt_file

        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this mode.

        Returns:
            The system prompt string.
        """
        return self.system_prompt

    @abstractmethod
    def get_mode_name(self) -> str:
        """
        Get the display name of this mode.

        Returns:
            The mode name (e.g., "Organisation", "Branding - Clara")
        """
        pass

    @abstractmethod
    def get_initial_message(self) -> Optional[str]:
        """
        Get the initial message to send when starting this mode.
        Some modes start with a bot message, others wait for user input.

        Returns:
            The initial message, or None if the mode waits for user input.
        """
        pass

    def update_score(self, delta: int) -> None:
        """
        Update the internal conviction score.

        Args:
            delta: Points to add (positive) or subtract (negative)
        """
        self.current_score = max(0, min(100, self.current_score + delta))

    def get_score(self) -> int:
        """
        Get the current conviction score.

        Returns:
            Score between 0 and 100.
        """
        return self.current_score

    def reset_score(self) -> None:
        """Reset the score to 0."""
        self.current_score = 0

    def should_end_session(self, message: str) -> bool:
        """
        Check if the bot's message indicates the session should end.
        This looks for the official decision marker in the bot's response.

        Args:
            message: The bot's message to check

        Returns:
            True if the session should end (decision made)
        """
        # Only check for the official decision format used in all prompts
        # This prevents false positives when words like "achat", "refus", or "hésitation"
        # appear in normal conversation context
        return "📊 DÉCISION :" in message or "📊 DECISION :" in message

    async def handle_message(
        self,
        user_message: str,
        conversation_history: list,
        ai_client
    ) -> str:
        """
        Handle a user message and generate a response.

        Args:
            user_message: The user's message
            conversation_history: List of previous messages
            ai_client: The AI client to use for generation

        Returns:
            The bot's response
        """
        # Build the messages array for the AI
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]

        # Add conversation history
        messages.extend(conversation_history)

        # Add the new user message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = await ai_client.generate_response(
            messages=messages,
            max_tokens=1000,
            temperature=0.85
        )

        return response
