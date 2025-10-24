from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Veritabanı tablolarını oluşturur"""
    from .models import User, Conversation, Message  # import edilmeyen modellerı bilemez vve tablelarını oluşturamaz
    Base.metadata.create_all(bind=engine)

def get_db():
    """Database session dependency - FastAPI route'larında kullanılır"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Tüm tabloları oluşturur"""
    from src.api.database.models import User, Conversation, Message
    Base.metadata.create_all(bind=engine)
