import os

from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = str(os.getenv("TEST_DATABASE_URL", "sqlite://:memory:"))
DATABASE_URL = str(os.getenv("DATABASE_URL"))

CORS_ALLOWED_ORIGINS = os.environ["CORS_ALLOWED_ORIGINS"].split(",")

JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
JWT_ACCESS_SECRET = os.environ["JWT_ACCESS_SECRET"]
JWT_ACCESS_EXPIRY = float(os.getenv("JWT_ACCESS_EXPIRY", 15))
JWT_REFRESH_SECRET = os.environ["JWT_REFRESH_SECRET"]
JWT_REFRESH_EXPIRY = float(os.getenv("JWT_REFRESH_EXPIRY", 7))