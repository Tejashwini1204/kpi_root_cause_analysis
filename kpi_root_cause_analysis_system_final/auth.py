import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")
conn.commit()


def signup_user(username, password):

    existing = c.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if existing:
        return False

    c.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()
    return True


def login_user(username, password):

    user = c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    return user