"""Command registry and execution for Jarvis."""

import subprocess
import webbrowser
import os
from datetime import datetime
from loguru import logger
from typing import Callable, Dict, Optional


class CommandRegistry:
    """Manages custom commands for Jarvis."""

    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self._register_default_commands()

    def _register_default_commands(self) -> None:
        """Register built-in commands."""
        self.register("time", self._cmd_time, "Tell the current time")
        self.register("date", self._cmd_date, "Tell the current date")
        self.register("open", self._cmd_open, "Open an application (e.g., 'open notepad')")
        self.register("search", self._cmd_search, "Search on Google (e.g., 'search python tutorials')")
        self.register("weather", self._cmd_weather, "Get weather info (requires API)")

    def register(self, name: str, func: Callable, description: str = "") -> None:
        """Register a new command."""
        self.commands[name.lower()] = func
        logger.info(f"✅ Command registered: {name} - {description}")

    def execute(self, command: str, *args) -> Optional[str]:
        """Execute a command."""
        cmd_name = command.lower().split()[0]
        if cmd_name in self.commands:
            try:
                logger.info(f"🚀 Executing command: {command}")
                return self.commands[cmd_name](*args)
            except Exception as e:
                logger.error(f"❌ Command execution failed: {e}")
                return f"Error executing command: {e}"
        else:
            logger.warning(f"Unknown command: {command}")
            return f"Unknown command: {cmd_name}"

    @staticmethod
    def _cmd_time() -> str:
        """Get current time."""
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def _cmd_date() -> str:
        """Get current date."""
        return datetime.now().strftime("%A, %B %d, %Y")

    @staticmethod
    def _cmd_open(app: str) -> str:
        """Open an application."""
        try:
            subprocess.Popen(app)
            return f"Opening {app}..."
        except Exception as e:
            return f"Could not open {app}: {e}"

    @staticmethod
    def _cmd_search(query: str) -> str:
        """Search Google."""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching for {query}..."

    @staticmethod
    def _cmd_weather() -> str:
        """Placeholder for weather command."""
        return "Weather command not yet implemented. Add your API key to enable."

    def list_commands(self) -> str:
        """List all available commands."""
        return "\n".join(self.commands.keys())
