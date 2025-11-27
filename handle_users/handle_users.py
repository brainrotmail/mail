import secrets
import string

import sqlite3


def generate_username() -> str:
    alphabet = string.ascii_letters
    username = "".join(secrets.choice(alphabet) for i in range(8))
    return username


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password



def databaseaddstuff():

    urlplaceholder = "www.example.com"

    username = generate_username()
    password = generate_password()

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT,
        website TEXT
    )
    """)

    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, urlplaceholder))
    con.commit()
    con.close()