import clipboard
import sqlite3 as sql
import time
from pynput import keyboard
from tkinter import *
ROOT = Tk()

HOTKEY = '<ctrl>+c'
CURRENT_DATETIME = time.asctime(time.localtime())
DB_PATH = 'clipboard.db'


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


def view_data():
    view = sql.connect(DB_PATH)
    cursor = view.cursor()
    cursor.execute("SELECT * FROM clipboard")
    rows = cursor.fetchall()
    view.commit()
    for row in rows:
        print(row)


def delete_all_data():
    delete = sql.connect(DB_PATH)
    cursor = delete.cursor()
    cursor.execute("DELETE FROM clipboard")
    delete.commit()


button_exit = Button(ROOT, text="Exit", command=quit)
button_refresh = Button(ROOT, text="Show Clipboard", command=view_data)
button_delete_all = Button(ROOT, text="Delete All", command=delete_all_data)

button_exit.pack()
button_refresh.pack()
button_delete_all.pack()


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse(HOTKEY),
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    ROOT.mainloop()
    listener.join()
