"""Database settings. Edit the password to match your MySQL root password."""
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "MySQL@Stu26#Db",
    "database": "student_db",
}

# Set to True to use a local SQLite file instead of MySQL (handy for testing).
USE_SQLITE = False
SQLITE_FILE = "student_local.db"
