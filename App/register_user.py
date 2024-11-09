import hashlib  # For hashing the eID with salt
import bcrypt   # For secure password hashing
import os       # For generating a random salt

# Important Notes:
# - Adding a salt to the eID provides additional security by ensuring that identical eID values result in unique hashes.
# - bcrypt is used to hash passwords securely with a unique salt for each user, following best practices for password storage.



# Function to hash the eID with a unique salt
def hash_eid_with_salt(eid):
    # Generate a unique salt for each `eID`
    salt = os.urandom(16)  # 16 bytes is a standard size for a salt
    # Concatenate the salt and eID, then hash with SHA-256
    eid_hash = hashlib.sha256(salt + eid.encode()).hexdigest()
    return eid_hash, salt

# Register a new user with a salted and hashed eID, username, and password
def register_user(eid, username, password):
    eid_hash, salt = hash_eid_with_salt(eid)
    
    # Check if the eID hash is already registered
    cursor.execute("SELECT * FROM users WHERE eID_hash = ?", (eid_hash,))
    if cursor.fetchone():
        print("This eID is already registered. Multiple accounts are not allowed.")
        return
    
    # Hash and salt the password securely with bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert the new user into the database, storing the eID hash and salt
    cursor.execute("INSERT INTO users (eID_hash, salt, username, password_hash) VALUES (?, ?, ?, ?)", (eid_hash, salt, username, password_hash))
    conn.commit()
    print("User registered successfully.")

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

# Function to authenticate a user with username and password
def login_user(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        print("Login successful!")
    else:
        print("Invalid credentials.")

# Example usage
eid = "unique_eid_from_initial_eID_verification"  # Replace with the actual unique identifier from eID verification
username = "user123"
password = "secure_password"

register_user(eid, username, password)  # Register user with salted and hashed eID, username, and password
is_eid_registered(eid)                  # Check if eID is registered
login_user(username, password)          # User logs in with username and password
