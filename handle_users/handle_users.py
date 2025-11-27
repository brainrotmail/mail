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



def makebatch():
    folder_id = str(uuid.uuid4())
    return folder_id


DB_PATH = "credentials.db"

def init_database():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS folders (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            type INTEGER NOT NULL,
            name TEXT NOT NULL,
            folder_id TEXT,
            username TEXT,
            password TEXT,
            uri TEXT,
            FOREIGN KEY (folder_id) REFERENCES folders (id)
        )
    """)

    conn.commit()
    conn.close()

def add_folder(folder_id, name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO folders (id, name)
        VALUES (?, ?)
    """, (folder_id, name))

    conn.commit()
    conn.close()

def add_item(name, folder_id, username, password, uri, item_type=1):
    item_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items (id, type, name, folder_id, username, password, uri)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (item_id, item_type, name, folder_id, username, password, uri))

    conn.commit()
    conn.close()

    return item_id

def export_to_json(output_path="export.json"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM folders")
    folders_data = cursor.fetchall()

    folders = [{"id": row[0], "name": row[1]} for row in folders_data]

    cursor.execute("""
        SELECT id, type, name, folder_id, username, password, uri
        FROM items
    """)
    items_data = cursor.fetchall()

    items = []
    for row in items_data:
        item = {
            "id": row[0],
            "type": row[1],
            "name": row[2],
            "folderId": row[3],
            "login": {
                "username": row[4],
                "password": row[5],
                "uris": [{"uri": row[6]}] if row[6] else []
            }
        }
        items.append(item)

    output = {
        "folders": folders,
        "items": items
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)

    conn.close()
    return output_path



def createdatabase():
    init_database()
    add_folder(makebatch(), "tiny.cc")