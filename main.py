import clipboard
import sqlite3 as sql
import time
from pynput import keyboard
from tkinter import *
ROOT = Tk()

HOTKEY = '<ctrl>+c'
CURRENT_DATETIME = time.asctime(time.localtime())
DB_PATH = 'clipboard.db'


def check_conn():
    try:
        conn.cursor()
        return True
    except Exception:
        return False


if not check_conn():
    conn = sql.connect(DB_PATH)
conn.cursor().execute(
    "CREATE TABLE IF NOT EXISTS clipboard (id INTEGER PRIMARY KEY, content TEXT NOT NULL, datetime TEXT NOT NULL)")
getTable = conn.cursor().execute(
  """SELECT name FROM sqlite_master WHERE type='table'
  AND name='clipboard'; """).fetchall()
if getTable != []:
    conn.commit()
conn.close()


def on_activate():
    data = clipboard.paste()
    save_clipboard(data)


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


def save_clipboard(data):
    global CURRENT_DATETIME
    if not check_conn():
        conn = sql.connect(DB_PATH)
    conn.cursor().execute("INSERT INTO clipboard (content, datetime) VALUES (?, ?)",
                          (data, CURRENT_DATETIME))
    conn.commit()
    print("Saved: " + data)


def view_data():
    if check_conn():
        conn.close()
    view = sql.connect(DB_PATH)
    view.cursor().execute("SELECT * FROM clipboard")
    rows = view.cursor().fetchall()
    for row in rows:
        print(row)


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse(HOTKEY),
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    listener.join()


button_exit = Button(root, text="Exit", command=ROOT.quit)
button_refresh = Button(root, text="Refresh", command=view_data)

button_exit.pack()
button_refresh.pack()
ROOT.mainloop()
