from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext, ttk

from .command_processor import CommandProcessor, CommandResult
from .voice_engine import VoiceEngine


class VoiceAssistantApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Python Voice Assistant")
        self.root.geometry("760x560")
        self.root.minsize(640, 480)

        self.command_processor = CommandProcessor()
        self.voice_engine = VoiceEngine()
        self.speak_replies = tk.BooleanVar(value=True)
        self.status_text = tk.StringVar(value="Ready")
        self.input_text = tk.StringVar()

        self._configure_style()
        self._build_layout()
        self._add_message("Assistant", "Hello! Type a command or use the microphone button. Say help to see commands.")

    def run(self) -> None:
        self.root.mainloop()

    def _configure_style(self) -> None:
        self.root.configure(bg="#f4f7fb")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f7fb")
        style.configure("Header.TLabel", background="#f4f7fb", foreground="#172033", font=("Segoe UI", 20, "bold"))
        style.configure("Subtle.TLabel", background="#f4f7fb", foreground="#607087", font=("Segoe UI", 10))
        style.configure("Status.TLabel", background="#e7eef8", foreground="#253246", padding=(10, 6), font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
        style.configure("Accent.TButton", background="#2867d8", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1f57bb")])
        style.configure("TCheckbutton", background="#f4f7fb", foreground="#253246", font=("Segoe UI", 10))

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=18)
        container.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(container)
        header.pack(fill=tk.X)

        title_block = ttk.Frame(header)
        title_block.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(title_block, text="Python Voice Assistant", style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(
            title_block,
            text="Voice commands, typed commands, notes, quick actions, and spoken replies.",
            style="Subtle.TLabel",
        ).pack(anchor=tk.W, pady=(2, 0))

        ttk.Label(header, textvariable=self.status_text, style="Status.TLabel").pack(side=tk.RIGHT)

        self.history = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            height=18,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#182235",
            relief=tk.FLAT,
            padx=12,
            pady=12,
        )
        self.history.pack(fill=tk.BOTH, expand=True, pady=(18, 12))
        self.history.configure(state=tk.DISABLED)

        input_row = ttk.Frame(container)
        input_row.pack(fill=tk.X)

        self.command_entry = ttk.Entry(input_row, textvariable=self.input_text, font=("Segoe UI", 11))
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", lambda _event: self._submit_text_command())
        self.command_entry.focus()

        ttk.Button(input_row, text="Send", style="Accent.TButton", command=self._submit_text_command).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(input_row, text="Mic", command=self._listen).pack(side=tk.LEFT, padx=(8, 0))

        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(12, 0))
        ttk.Checkbutton(actions, text="Speak replies", variable=self.speak_replies).pack(side=tk.LEFT)

        for label, command in (
            ("Help", "help"),
            ("Time", "what time is it"),
            ("Date", "what is today's date"),
            ("Notes", "show notes"),
            ("Joke", "tell me a joke"),
            ("Clear", "clear"),
        ):
            ttk.Button(actions, text=label, command=lambda value=command: self._process_command(value)).pack(side=tk.LEFT, padx=(8, 0))

    def _submit_text_command(self) -> None:
        command = self.input_text.get().strip()
        self.input_text.set("")
        self._process_command(command)

    def _listen(self) -> None:
        self.status_text.set("Starting microphone...")
        self.voice_engine.listen_async(
            on_success=lambda command: self.root.after(0, self._process_command, command),
            on_error=lambda message: self.root.after(0, self._show_error, message),
            on_status=lambda message: self.root.after(0, self.status_text.set, message),
        )

    def _process_command(self, command: str) -> None:
        if not command:
            return

        self.status_text.set("Processing...")
        self._add_message("You", command)
        result = self.command_processor.handle(command)
        self._handle_result(result)

    def _handle_result(self, result: CommandResult) -> None:
        if result.clear_history:
            self._clear_history()

        self._add_message("Assistant", result.response)
        self.status_text.set("Ready")

        if self.speak_replies.get():
            self.voice_engine.speak(result.response)

        if result.should_exit:
            self.root.after(900, self.root.destroy)

    def _show_error(self, message: str) -> None:
        self.status_text.set("Ready")
        self._add_message("Assistant", message)

    def _add_message(self, sender: str, message: str) -> None:
        self.history.configure(state=tk.NORMAL)
        self.history.insert(tk.END, f"{sender}: {message}\n\n")
        self.history.see(tk.END)
        self.history.configure(state=tk.DISABLED)

    def _clear_history(self) -> None:
        self.history.configure(state=tk.NORMAL)
        self.history.delete("1.0", tk.END)
        self.history.configure(state=tk.DISABLED)
