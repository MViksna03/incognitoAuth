import bcrypt   # For secure password hashing
import sqlite3  # Database for storing user info
from hash_eid import hash_eid

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Register a new user with a salted and hashed eID, username, and password
def register_user(eid, username, password):
    eid_hash, salt = hash_eid(eid)
    
    # Hash and salt the password securely with bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert the new user into the database, storing the eID hash and salt
    cursor.execute("INSERT INTO users (eID_hash, salt, username, password_hash) VALUES (?, ?, ?, ?)", (eid_hash, salt, username, password_hash))
    conn.commit()
    print("User registered successfully.")

