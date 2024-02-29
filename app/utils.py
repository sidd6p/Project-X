from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def is_correct_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
