from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)


def verify_pass(password: str, hashed_pass: str) -> str:
    return pwd_context.verify(password, hashed_pass)


def generate_ref() -> str:
    return uuid.uuid4()
