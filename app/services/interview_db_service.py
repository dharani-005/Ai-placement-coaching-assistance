import sqlite3

DB = "interview.db"


def init_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asked_questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT
    )
    """)

    conn.commit()
    conn.close()


def clear_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM asked_questions")

    conn.commit()
    conn.close()


def store_question(question):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO asked_questions(question) VALUES(?)",
        (question,)
    )

    conn.commit()
    conn.close()


def get_asked_questions():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT question FROM asked_questions")

    rows = cursor.fetchall()

    conn.close()

    return [r[0] for r in rows]