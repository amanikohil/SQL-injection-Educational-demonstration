import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

users = [
    ("002345678", "pwd"),
    ("009876543", "pwd"),
    ("001112223", "pwd"),
    ("004455667", "pwd"),
    ("007778889", "pwd"),
    ("003333444", "pwd"),
    ("008888999", "pwd"),
    ("005551234", "pwd"),
    ("006666777", "pwd"),
    ("009990001", "pwd"),
]

for user in users:
    try:
        cur.execute("INSERT INTO users (ccp_code, password) VALUES (?, ?)", user)
    except sqlite3.IntegrityError:
        pass  # skip if already exists

conn.commit()
conn.close()

print("Users inserted successfully!")