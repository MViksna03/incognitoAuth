import sqlite3  # Database for storing user info
from hash_eid import hash_eid
import hashlib

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

"""
def is_eid_registered(eid):
    eid_hash, salt = hash_eid(eid)
    # Check if the eID hash is already registered
    cursor.execute("SELECT * FROM users WHERE eID_hash = ?", (eid_hash,))
    if cursor.fetchone():
        print("This eID is already registered. Multiple accounts are not allowed.")
        return True
    return False
"""


# Function to verify if an eID is already registered

def is_eid_registered(eid):
    # Query for all stored eID_hash and salt pairs
    cursor.execute("SELECT eID_hash, salt FROM users")
    for stored_hash, stored_salt in cursor.fetchall():
        # Hash the provided eID with each retrieved salt
        test_hash = hashlib.sha256(stored_salt + eid.encode()).hexdigest()
        if test_hash == stored_hash:
            print("eID is already registered.")
            return True
    print("eID is not registered.")
    return False

    