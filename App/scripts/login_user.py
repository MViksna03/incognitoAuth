import bcrypt   # For secure password hashing
import sqlite3  # Database for storing user info

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

def login_user():
    return True


# Function to authenticate a user with username and password
def login_user(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True
    else:
        return False