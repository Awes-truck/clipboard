import clipboard
import sqlite3 as sql
import time
from pynput import keyboard

from tkinter import *
ROOT = Tk()
ROOT.title("Clipboard")
ROOT.configure(background="#060608")

HOTKEY = '<ctrl>+c'
CURRENT_DATETIME = time.asctime(time.localtime())
DB_PATH = 'clipboard.db'
ALL_DATA = ""


def check_conn(connection):
    try:
        connection.cursor()
        return True
    except Exception:
        return False


conn = sql.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS clipboard (id INTEGER PRIMARY KEY, content TEXT NOT NULL, datetime TEXT NOT NULL)")
getTable = cursor.execute(
  """SELECT name FROM sqlite_master WHERE type='table'
  AND name='clipboard'; """).fetchall()
if getTable != []:
    conn.commit()
conn.close()


def on_activate():
    save_clipboard()


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


def save_clipboard():
    global CURRENT_DATETIME
    data = clipboard.paste()
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clipboard (content, datetime) VALUES (?, ?)", (data, CURRENT_DATETIME))
    conn.commit()
    print("Saved: " + data)


def refresh_clipboard():
    global ALL_DATA
    ALL_DATA = ""
    textbox.delete(1.0, END)
    view = sql.connect(DB_PATH)
    #conn.row_factory = sql.Row
    cursor = view.cursor()
    cursor.execute("SELECT * FROM clipboard")
    rows = cursor.fetchall()
    view.commit()
    for row in rows:
        ALL_DATA += (str(row) + "\n")
    print(ALL_DATA)
    textbox.insert(END, ALL_DATA)


def delete_all_data():
    global ALL_DATA
    delete = sql.connect(DB_PATH)
    cursor = delete.cursor()
    cursor.execute("DELETE FROM clipboard")
    delete.commit()
    ALL_DATA = ""


Label(ROOT, text="Welcome to Clipboard").grid(row=0, column=0, sticky=E)

Button(ROOT, text="Refresh Clipboard", fg="#fff", bg="#060608", command=refresh_clipboard).grid(
    row=0, column=0, sticky=W)
Button(ROOT, text="Delete All", fg="#fff", bg="#060608", command=delete_all_data).grid(
    row=0, column=2, sticky=W)
Button(ROOT, text="Exit", padx=20, fg="#fff", bg="#060608", command=quit).grid(
    row=0, column=3, sticky=E)

textbox = Text(ROOT, width=120, height=20, wrap=WORD, background="gray")
textbox.grid(row=2, column=0, sticky=E)

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse(HOTKEY),
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    ROOT.mainloop()
    listener.join()
