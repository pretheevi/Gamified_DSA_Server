from passlib.context import CryptContext

# Create a CryptContext object with the desired hashing algorithm and options
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    :param password: The password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)

# Function to verify a password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.
    
    :param plain_password: The plain password to verify.
    :param hashed_password: The hashed password to check against.
    :return: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)