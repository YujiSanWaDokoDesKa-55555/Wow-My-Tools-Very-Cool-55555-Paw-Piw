import os
import sys
import time
import termios
import shutil
import subprocess
import atexit
import select

MIN_COLS = 53

a = "\033[1;30m"
m = "\033[1;31m"
h = "\033[1;32m"
k = "\033[1;33m"
c = "\033[1;36m"
p = "\033[1;37m"
r = "\033[0m"

def hide_cursor():
    print("\033[?25l", end="", flush=True)

def show_cursor():
    print("\033[?25h", end="", flush=True)

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

atexit.register(show_cursor)

def restore_terminal():
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except:
        pass

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

def check_for_updates():
    try:
        subprocess.run(
            ["git", "pull"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )
    except:
        pass

os.system("clear")

try:
    new_settings = termios.tcgetattr(fd)
    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
    hide_cursor()

    last_status = None

    while True:
        cols = shutil.get_terminal_size().columns

        if cols >= MIN_COLS:
            status = (
                "OK",
                f"""
\033[102m   {r} {p}Ukuran Layar {h}Sudah{p} Sesuai. Silahkan Klik Huruf Y"""
            )
        else:
            status = (
                "SMALL",
                f"""
\033[101m   {r} {p}Ukuran Layar {m}Belum{p} Sesuai. Silahkan Cubit Layar"""
            )

        if status != last_status:
            print("\033[2J\033[H", end="", flush=True)
            print(status[1], end="", flush=True)
            last_status = status

        if cols >= MIN_COLS:
            key = get_key()
            if key and key.lower() == "y":
                restore_terminal()
                show_cursor()

                check_for_updates()

                print("\033[2J\033[H", end="", flush=True)
                subprocess.run(
                    [sys.executable, "epx.py"],
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr
                )
                sys.exit()

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    restore_terminal()
    show_cursor()