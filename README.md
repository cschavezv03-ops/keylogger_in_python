# Python Keylogger

A small, educational keylogger written in Python with
[`pynput`](https://pypi.org/project/pynput/). It listens for global keyboard
events and appends what you type to `log.txt`, flushing the buffer every 10
keystrokes.

> **Disclaimer:** this project is for learning about input hooks and security
> concepts only. Do not run it on a machine you do not own or without the
> explicit consent of its user. Logging someone else's keystrokes is illegal in
> most jurisdictions.

## Features

- Global keyboard capture on supported platforms.
- Buffers 10 keystrokes before writing, so the file is not opened on every key.
- `Space` is written as a newline.
- Special keys (`Shift`, `Ctrl`, `Enter`, arrows, ...) are ignored.
- `Esc` stops the listener.
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

The file is written every 10 keystrokes. A trailing group of fewer than 10
keys stays in memory until the buffer fills up again.

## How it works

| Function | Purpose |
| --- | --- |
| `on_press(key)` | Adds the key to the buffer, prints it, and calls `write_file` every 10 keystrokes. |
| `write_file(keys)` | Appends the buffered keys to `log.txt`. `Key.space` becomes `\n`; keys whose name starts with `Key.` are skipped. |
| `on_release(key)` | Returns `False` when `Esc` is released, which stops the listener. |

Character keys are converted with `str(key).replace("'", "")`, so `'a'`
becomes `a`. Named keys are represented as `Key.enter`, `Key.shift`, etc.,
which is why they can be filtered with `startswith("Key.")`.

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

- **`log.txt` is empty or missing:** you may have typed fewer than 10 keys, the
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
