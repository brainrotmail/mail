import secrets
import sqlite3
import string


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


def databaseaddstuff(url: str, batch: str):
    con = sqlite3.connect("credentials.db")
    cur = con.cursor()

    cur.execute(f"CREATE TABLE IF NOT EXISTS {batch}(username, password, website)")

    username = generate_username()
    password = generate_password()

    cur.execute(f"INSERT INTO {batch} VALUES (?, ?, ?)", (username, password, url))
    con.commit()
    con.close()

    class User:
        def __init__(self):
            self.name = username
            self.password = password

    def get_user() -> User:
        return User()

    return get_user()
