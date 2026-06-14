from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import random
import subprocess
import webbrowser


@dataclass
class CommandResult:
    response: str
    should_exit: bool = False
    clear_history: bool = False


@dataclass
class CommandProcessor:
    notes: list[str] = field(default_factory=list)

    def handle(self, raw_command: str) -> CommandResult:
        command = " ".join(raw_command.lower().strip().split())

        if not command:
            return CommandResult("Please type or say a command.")

        if command in {"exit", "quit", "close assistant", "goodbye"}:
            return CommandResult("Goodbye. Have a productive day!", should_exit=True)

        if command in {"clear", "clear chat", "clear history"}:
            return CommandResult("Conversation cleared.", clear_history=True)

        if "help" in command or command == "commands":
            return CommandResult(self._help_text())

        if "time" in command:
            return CommandResult(f"The current time is {datetime.now().strftime('%I:%M %p')}.")

        if "date" in command or "day" in command:
            return CommandResult(f"Today is {datetime.now().strftime('%A, %d %B %Y')}.")

        if command.startswith(("take note", "note", "remember")):
            return self._take_note(raw_command)

        if command in {"show notes", "read notes", "my notes"}:
            return self._show_notes()

        if command in {"clear notes", "delete notes"}:
            self.notes.clear()
            return CommandResult("All notes have been cleared.")

        if command.startswith(("search ", "google ")):
            query = command.replace("search ", "", 1).replace("google ", "", 1).strip()
            return self._open_url(f"https://www.google.com/search?q={query.replace(' ', '+')}", f"Searching Google for {query}.")

        if command.startswith("open "):
            return self._open_target(command.replace("open ", "", 1).strip())

        if "joke" in command:
            return CommandResult(random.choice(self._jokes()))

        return CommandResult(
            "I did not understand that command. Try saying help to see what I can do."
        )

    def _take_note(self, raw_command: str) -> CommandResult:
        lowered = raw_command.lower()
        for prefix in ("take note", "remember", "note"):
            if lowered.startswith(prefix):
                note = raw_command[len(prefix):].strip(" :,-")
                break
        else:
            note = raw_command.strip()

        if not note:
            return CommandResult("What should I write in the note?")

        self.notes.append(note)
        return CommandResult(f"Saved note: {note}")

    def _show_notes(self) -> CommandResult:
        if not self.notes:
            return CommandResult("You do not have any notes yet.")

        note_text = "\n".join(f"{index}. {note}" for index, note in enumerate(self.notes, start=1))
        return CommandResult(f"Here are your notes:\n{note_text}")

    def _open_target(self, target: str) -> CommandResult:
        websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "linkedin": "https://www.linkedin.com",
        }
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
        }

        if target in websites:
            return self._open_url(websites[target], f"Opening {target}.")

        if target in apps:
            try:
                subprocess.Popen([apps[target]], shell=False)
            except OSError as error:
                return CommandResult(f"I could not open {target}: {error}")
            return CommandResult(f"Opening {target}.")

        if "." in target and " " not in target:
            url = target if target.startswith(("http://", "https://")) else f"https://{target}"
            return self._open_url(url, f"Opening {target}.")

        return CommandResult("I can open Google, YouTube, GitHub, Gmail, LinkedIn, Notepad, Calculator, or Paint.")

    @staticmethod
    def _open_url(url: str, response: str) -> CommandResult:
        webbrowser.open(url)
        return CommandResult(response)

    @staticmethod
    def _help_text() -> str:
        return (
            "You can ask me to:\n"
            "- tell the time or date\n"
            "- take note your message\n"
            "- show notes or clear notes\n"
            "- search any topic\n"
            "- open Google, YouTube, GitHub, Gmail, LinkedIn, Notepad, Calculator, or Paint\n"
            "- tell a joke\n"
            "- clear chat or exit"
        )

    @staticmethod
    def _jokes() -> list[str]:
        return [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "I told my computer I needed a break, and it said no problem, it would go to sleep.",
            "Why was the function calm? Because it knew how to return.",
        ]
