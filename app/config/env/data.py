import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_MIGRATION = os.getenv("DATABASE_URL_MIGRATION")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", 0))

AZ_BLOB_ACCOUNT_NAME = os.getenv("AZ_BLOB_ACCOUNT_NAME")
AZ_BLOB_ACCOUNT_KEY = os.getenv("AZ_BLOB_ACCOUNT_KEY")
AZ_BLOB_CONTAINER_NAME = os.getenv("AZ_BLOB_CONTAINER_NAME")
