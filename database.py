import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)")
        self.conn.commit()

    def insert(self, telegram_id, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?, ?)", (telegram_id, username, password))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def search_username(self, username=""):
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        rows = self.cur.fetchall()
        return rows
    
    def search_telegram_id(self, telegram_id=""):
        self.cur.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM users WHERE id=?", (id,))
        self.conn.commit()

    def update(self, telegram_id, password):
        self.cur.execute("SELECT rowid FROM  users WHERE telegram_id=?", (telegram_id,))
        _id = self.cur.fetchone()[0]
        self.cur.execute("UPDATE users SET password=? WHERE rowid=?", (password, _id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()