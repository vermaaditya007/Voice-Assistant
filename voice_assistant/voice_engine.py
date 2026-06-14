from __future__ import annotations

import threading
from typing import Callable


class VoiceEngine:
    def __init__(self) -> None:
        self._speech_recognition = None
        self._recognizer = None
        self._microphone = None
        self._tts = None
        self.voice_available = False
        self.speech_available = False
        self._load_voice_input()
        self._load_text_to_speech()

    def listen_async(
        self,
        on_success: Callable[[str], None],
        on_error: Callable[[str], None],
        on_status: Callable[[str], None],
    ) -> None:
        thread = threading.Thread(
            target=self._listen_worker,
            args=(on_success, on_error, on_status),
            daemon=True,
        )
        thread.start()

    def speak(self, text: str) -> None:
        if not self.speech_available or self._tts is None:
            return

        thread = threading.Thread(target=self._speak_worker, args=(text,), daemon=True)
        thread.start()

    def _load_voice_input(self) -> None:
        try:
            import speech_recognition as sr
        except ImportError:
            return

        try:
            self._speech_recognition = sr
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone
            self.voice_available = True
        except (OSError, AttributeError):
            self.voice_available = False

    def _load_text_to_speech(self) -> None:
        try:
            import pyttsx3
        except ImportError:
            return

        try:
            self._tts = pyttsx3.init()
            self._tts.setProperty("rate", 170)
            self._tts.setProperty("volume", 0.9)
            self.speech_available = True
        except RuntimeError:
            self.speech_available = False

    def _listen_worker(
        self,
        on_success: Callable[[str], None],
        on_error: Callable[[str], None],
        on_status: Callable[[str], None],
    ) -> None:
        if not self.voice_available or self._recognizer is None or self._microphone is None:
            on_error("Voice input is unavailable. Install SpeechRecognition and PyAudio, then check your microphone.")
            return

        sr = self._speech_recognition
        on_status("Listening...")

        try:
            with self._microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=8)
            on_status("Recognizing...")
            command = self._recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            on_error("I did not hear anything. Please try again.")
            return
        except sr.UnknownValueError:
            on_error("I could not understand the audio.")
            return
        except sr.RequestError:
            on_error("Speech recognition service is unavailable. Check your internet connection.")
            return
        except OSError as error:
            on_error(f"Microphone error: {error}")
            return

        on_success(command)

    def _speak_worker(self, text: str) -> None:
        try:
            self._tts.say(text)
            self._tts.runAndWait()
        except RuntimeError:
            self.speech_available = False
