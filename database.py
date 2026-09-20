import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
MYSQL_SSL_CA = os.getenv("MYSQL_SSL_CA")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

if not MYSQL_SSL_CA:
    raise RuntimeError("MYSQL_SSL_CA is not configured")

CA_PATH = "/tmp/aiven-ca.pem"

with open(CA_PATH, "w", encoding="utf-8") as f:
    f.write(MYSQL_SSL_CA)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": CA_PATH
        }
    }
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base.metadata.create_all(engine)