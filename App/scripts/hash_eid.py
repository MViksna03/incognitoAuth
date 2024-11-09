import os       # For generating a random salt
import hashlib

# Function to hash the eID with a unique salt
def hash_eid(eid):
    # Generate a unique salt for each `eID`
    salt = os.urandom(16)  # 16 bytes is a standard size for a salt
    # Concatenate the salt and eID, then hash with SHA-256
    eid_hash = hashlib.sha256(salt + eid.encode()).hexdigest()
    return eid_hash, salt