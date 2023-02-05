import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL, password TEXT NOT NULL)")
        self.conn.commit()

    def insert(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def search(self, username=""):
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM users WHERE id=?", (id,))
        self.conn.commit()

    def update(self, username, password):
        self.cur.execute("SELECT rowid FROM  users WHERE username=?", (username,))
        _id = self.cur.fetchone()[0]
        self.cur.execute("UPDATE users SET password=? WHERE rowid=?", (password, _id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()