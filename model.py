"""MODEL - data and database access (the Python equivalent of JDBC).

mysql-connector-python plays the role JDBC plays in Java:
connect -> cursor (Statement) -> execute -> fetch -> close.
"""
import re
import config

if config.USE_SQLITE:
    import sqlite3
    PLACEHOLDER = "?"
else:
    import mysql.connector
    PLACEHOLDER = "%s"


class Student:
    """Plain data object for one student."""

    def __init__(self, name, reg_no, student_id=None):
        self.id = student_id
        self.name = name
        self.reg_no = reg_no


class StudentModel:
    REG_PATTERN = re.compile(r"^RA\d{13}$")   # e.g. RA2511003011320

    def __init__(self):
        self.conn = self._connect()
        self._create_table()

    # ---------- connection ----------
    def _connect(self):
        if config.USE_SQLITE:
            return sqlite3.connect(config.SQLITE_FILE)
        return mysql.connector.connect(**config.DB_CONFIG)

    def _create_table(self):
        cur = self.conn.cursor()
        if config.USE_SQLITE:
            cur.execute("""CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reg_no TEXT NOT NULL UNIQUE)""")
        else:
            cur.execute("""CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                reg_no VARCHAR(20) NOT NULL UNIQUE)""")
        self.conn.commit()
        cur.close()

    # ---------- validation ----------
    def validate(self, name, reg_no):
        if not name.strip():
            return "Name cannot be empty."
        if not re.fullmatch(r"[A-Za-z .]+", name.strip()):
            return "Name may contain only letters, spaces and dots."
        if not self.REG_PATTERN.match(reg_no.strip().upper()):
            return "Registration number must look like RA2511003011320."
        return None

    # ---------- CRUD ----------
    def add(self, student):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO student (name, reg_no) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
                    (student.name.strip(), student.reg_no.strip().upper()))
        self.conn.commit()
        cur.close()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, reg_no FROM student ORDER BY id")
        rows = [Student(n, r, i) for (i, n, r) in cur.fetchall()]
        cur.close()
        return rows

    def search(self, text):
        cur = self.conn.cursor()
        like = f"%{text.strip()}%"
        cur.execute(f"SELECT id, name, reg_no FROM student "
                    f"WHERE name LIKE {PLACEHOLDER} OR reg_no LIKE {PLACEHOLDER} ORDER BY id",
                    (like, like))
        rows = [Student(n, r, i) for (i, n, r) in cur.fetchall()]
        cur.close()
        return rows

    def update(self, student):
        cur = self.conn.cursor()
        cur.execute(f"UPDATE student SET name={PLACEHOLDER}, reg_no={PLACEHOLDER} WHERE id={PLACEHOLDER}",
                    (student.name.strip(), student.reg_no.strip().upper(), student.id))
        self.conn.commit()
        cur.close()

    def delete(self, student_id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM student WHERE id={PLACEHOLDER}", (student_id,))
        self.conn.commit()
        cur.close()

    def close(self):
        self.conn.close()
