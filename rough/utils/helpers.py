import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_pass(password: str) -> str:
    return pwd_context.hash(password)

def verify_pass(plain_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)

def generate_ref() -> str:
    uuid_v4 = uuid.uuid4()
    return uuid_v4
