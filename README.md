# Python Keylogger

A small, educational keylogger written in Python with
[`pynput`](https://pypi.org/project/pynput/). It listens for global keyboard
events and appends what you type to `log.txt`, one timestamped line per word.

> **Disclaimer:** this project is for learning about input hooks and security
> concepts only. Do not run it on a machine you do not own or without the
> explicit consent of its user. Logging someone else's keystrokes is illegal in
> most jurisdictions.

## Features

- Global keyboard capture on supported platforms.
- Buffers complete words and writes one line per word, with a timestamp of
  when the word started.
- A word is closed by `Space`, `Enter` or `Tab`.
- `Backspace` removes the last character of the word in progress.
- `Shift` produces uppercase letters.
- Keeps up to 10 finished lines in memory before opening the file.
- Special keys (`Ctrl`, `Alt`, arrows, ...) are ignored.
- `Esc` flushes everything pending and stops the listener, so no keystrokes
  are lost.
- Appends to `log.txt` instead of overwriting it.

## Requirements

- Python 3.8 or newer.
- [`pynput`](https://pypi.org/project/pynput/) 1.8 or newer.
- Operating system: Windows, macOS, or Linux with **X11**.

## Installation

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pynput
```

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pynput
```

If PowerShell blocks the activation script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Usage

```bash
python main.py
```

The program keeps running in the foreground. Type something, then press `Esc`
to stop it. The output is written to `log.txt` in the current working
directory:

```bash
cat log.txt        # Linux / macOS
type log.txt       # Windows
```

Output format is `<timestamp> | <word>`:

```
2026-10-24 16:06:35 | hola
2026-10-24 16:06:35 | mundo
2026-10-24 16:06:35 | MAYUSculas
```

The timestamp is taken when the first character of the word is typed, so two
words of the same sentence usually share it (seconds resolution). Words are
written to disk in groups of up to 10 lines, and anything still in memory is
flushed when you press `Esc`.

Punctuation stays attached to the word it follows (`hola,` is logged as
`hola,`), because only whitespace and `Enter`/`Tab` close a word.

## How it works

| Function | Purpose |
| --- | --- |
| `now()` | Returns the current time as `YYYY-MM-DD HH:MM:SS`. |
| `on_press(key)` | Tracks `Shift`, edits the word with `Backspace`, closes the word on `Space`/`Enter`/`Tab`, and appends characters. |
| `flush_word()` | Turns the word in progress into a `timestamp \| word` line. |
| `write_file()` | Appends the buffered lines to `log.txt` and empties the buffer. |
| `flush_all()` | Flushes the pending word and the buffer (on `Esc` and at exit). |
| `on_release(key)` | Clears `Shift`; returns `False` when `Esc` is released, which stops the listener. |

Character keys are read from `key.char` instead of `str(key)`, so `'a'`
becomes `a` and `Key.enter` has no `char` attribute (and is handled
separately). Named keys that are not explicitly handled are ignored.

Because the word buffer lives in memory, keystrokes typed into another
application between two word boundaries end up in the same line. That is the
expected trade-off for "log one line per word".

## Platform notes

### Linux

`pynput` uses the X11 `XRecord` extension. It works on an X11 session, but on
**Wayland** it can only see keystrokes sent to XWayland applications (for
example `xterm`); native Wayland windows are isolated by design. Check your
session with:

```bash
echo $XDG_SESSION_TYPE
```

If it prints `wayland`, test the keylogger from an X11 application such as
`xterm`, or use `evdev` (with `sudo`) for real global capture.

### Windows

Global capture works out of the box. Two caveats:

- To log keystrokes sent to applications running as administrator, run the
  script as administrator too (Windows UIPI blocks lower-integrity hooks).
- Windows Defender and other antivirus products may flag or quarantine the
  script because it behaves like spyware.

### macOS

Grant the terminal (or Python binary) permission in **System Settings >
Privacy & Security > Accessibility**, otherwise no events are delivered.

## Troubleshooting

- **`log.txt` is empty or missing:** you may not have closed a word yet (the
  word in progress is only written on `Space`/`Enter`/`Tab` or on `Esc`), the
  focused window may be a native Wayland window, or the process may not have
  permission to capture input.
- **`ModuleNotFoundError: No module named 'pynput'`:** the virtual environment
  is not activated. Run `.venv/bin/python main.py` (Linux/macOS) or
  `.\.venv\Scripts\python.exe main.py` (Windows).
- **Keys appear in the terminal but not in the file:** check the working
  directory, since `log.txt` is created relative to it.

## Project structure

```
.
├── main.py      # keylogger
├── log.txt      # generated output
├── LICENSE      # MIT license
└── README.md
```

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.
