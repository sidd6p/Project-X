import os

from dotenv import load_dotenv


load_dotenv()


class AppConfig:
    DB_HOST: str = os.getenv("DB_HOST")
    DB: str = os.getenv("DB")
    DB_USER: str = os.getenv("DB_USER")
    TEST_DB: str = os.getenv("TEST_DB")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_TIME_IN_MINUTE: int = int(os.getenv("JWT_EXPIRATION_TIME_IN_MINUTE"))


settings = AppConfig()
