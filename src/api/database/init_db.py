from src.api.database.database import create_tables, engine
from src.api.database.models import Base

def init_database():
    """Veritabanını başlatır ve tabloları oluşturur"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()