from utils.db import get_connection

def add_task(task):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks(task,status) VALUES (?,?)",
        (task,"Pending")
    )

    conn.commit()
    conn.close()

def get_tasks():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")

    data = cur.fetchall()

    conn.close()

    return data