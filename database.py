import sqlite3 as sql

class DatabaseHandler:
    def __init__(self,databaseName = "appData.db"):
        self.databaseName = databaseName

    def createTables(self):
        conn = sql.connect(self.databaseName)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                       username TEXT PRIMARY KEY NOT NULL,
                       password TEXT NOT NULL,
                       librarianPermissions BOOLEAN NOT NULL DEFAULT 0
                       )""")

        cursor.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        )
        table_sql = cursor.fetchone()
        if table_sql and "CHECK (length(password)" in table_sql[0]:
            cursor.execute("ALTER TABLE users RENAME TO users_old")
            cursor.execute("""CREATE TABLE users (
                           username TEXT PRIMARY KEY NOT NULL,
                           password TEXT NOT NULL,
                           librarianPermissions BOOLEAN NOT NULL DEFAULT 0
                           )""")
            cursor.execute("""INSERT INTO users
                           (username, password, librarianPermissions)
                           SELECT username, password,
                                  COALESCE(librarianPermissions, 0)
                           FROM users_old""")
            cursor.execute("DROP TABLE users_old")
        
        
        cursor.execute("PRAGMA foreign_keys = ON")
        conn.commit()
        conn.close()

    def createUser(self,username,password,librarianPermissions):
        try:
            conn = sql.connect(self.databaseName)
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO users
                   (username, password, librarianPermissions)
                   VALUES (?, ?, ?)""",
                (username, password,librarianPermissions),
            )
            conn.commit()
            return True,"signup successful"
        except sql.IntegrityError:
            return False, "an error occured signing up"
        finally:
            conn.close()

  