# Python Voice Assistant

A lightweight desktop voice assistant built with Python and Tkinter. It supports text commands, optional microphone input, text-to-speech replies, command history, quick actions, and a simple internship-friendly GUI.

## Features

- Light desktop GUI with assistant status, command input, and conversation history.
- Optional voice input using `SpeechRecognition`.
- Optional spoken replies using `pyttsx3`.
- Built-in commands for time, date, notes, web search, opening websites, opening common apps, jokes, help, and clearing history.
- Safe fallback mode: the app still works with typed commands if voice packages or microphone drivers are missing.

## Project Structure

```text
voice_assistant/
  __init__.py
  app.py
  command_processor.py
  voice_engine.py
main.py
requirements.txt
```

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

If `PyAudio` fails to install on Windows, install it with:

```powershell
pip install pipwin
pipwin install pyaudio
```

The assistant can still run without `PyAudio`; typed commands and text-to-speech will continue to work.

## Run

```powershell
python main.py
```

## Example Commands

- `help`
- `what time is it`
- `what is today's date`
- `take note internship presentation at 5 pm`
- `show notes`
- `clear notes`
- `search python tkinter voice assistant`
- `open youtube`
- `open google`
- `open notepad`
- `tell me a joke`
- `clear`
- `exit`

## Internship Demo Notes

This project demonstrates:

- GUI development with Tkinter.
- Speech recognition integration.
- Text-to-speech integration.
- Command parsing and action routing.
- Graceful error handling when optional hardware or packages are unavailable.
