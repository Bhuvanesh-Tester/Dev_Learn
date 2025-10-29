from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import binascii
from jose import jwt
import os

# ------------------------------------------------------------------
# ⚙️ Database & JWT configuration (for learning you can hardcode)
# ------------------------------------------------------------------
USER = "postgres.ixjbotjsmafnvfewfogn"
PASSWORD = "DBbhuvi@0007"
HOST = "aws-1-ap-south-1.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


JWT_SECRET = "learning_secret"  # use simple one for learning
JWT_ALGO = "HS256"

# ------------------------------------------------------------------
# 🧱 Database setup
# ------------------------------------------------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------------
# 🚀 FastAPI setup
# ------------------------------------------------------------------
app = FastAPI()

# Allow all origins (ok for learning)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# 📦 Models
# ------------------------------------------------------------------
class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

# ------------------------------------------------------------------
# 🔐 Utility functions
# ------------------------------------------------------------------
def hash_password(pw: str) -> str:
    # generate a 16-byte salt and derive a 32-byte key using PBKDF2-HMAC-SHA256
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 100000)
    # store salt + derived key as hex string
    return binascii.hexlify(salt + dk).decode()

def verify_password(plain, hashed) -> bool:
    try:
        data = binascii.unhexlify(hashed.encode())
        salt = data[:16]
        dk_stored = data[16:]
        dk_check = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt, 100000)
        return dk_check == dk_stored
    except Exception:
        return False

def create_token(data: dict):
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

# ------------------------------------------------------------------
# 🧩 Routes
# ------------------------------------------------------------------
@app.post("/api/register")
def register(payload: RegisterIn):
    db = SessionLocal()
