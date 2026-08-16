import hashlib

def hashed_password(password):
    password = "VaLen3n" + password
    return hashlib.sha256(password.encode()).hexdigest()