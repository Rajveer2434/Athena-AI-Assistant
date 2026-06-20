from utils.db import get_connection

def add_note(note):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes(note) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

def get_notes():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes")

    data = cur.fetchall()

    conn.close()

    return data