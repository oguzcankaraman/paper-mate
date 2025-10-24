from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional
from .models import User, Conversation, Message


# User CRUD Operations
def create_user(db: Session, name: str, email: str, password: str) -> User:
    """Yeni kullanıcı oluşturur."""
    db_user = User(
        name=name,
        email=email,
        password=password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:  # str -> int
    """ID'ye göre kullanıcı getirir."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Email'e göre kullanıcı getirir."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_name(db: Session, name: str) -> Optional[User]:
    """Name'e göre kullanıcı getirir."""
    return db.query(User).filter(User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[type[User]]:  # list[type[User]] -> list[User]
    """Tüm kullanıcıları getirir."""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:  # str -> int
    """Kullanıcı bilgilerini günceller."""
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:  # str -> int
    """Kullanıcıyı siler."""
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# Conversation CRUD Operations
def create_conversation(db: Session, user_id: int) -> Optional[Conversation]:  # str -> int, Optional ekle
    """Yeni konuşma oluşturur."""
    # Foreign key kontrolü
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    db_conversation = Conversation(user_id=user_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_conversation_by_id(db: Session, conversation_id: int) -> Optional[Conversation]:
    """ID'ye göre konuşma getirir."""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def get_conversations_by_user(db: Session, user_id: int) -> list[type[Conversation]]:  # str -> int, list[type[Conversation]] -> list[Conversation]
    """Kullanıcının tüm konuşmalarını getirir."""
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).all()


def update_conversation(db: Session, conversation_id: int, updated_at: datetime = None) -> Optional[Conversation]:
    """Konuşmanın updated_at zamanını günceller."""
    conversation = get_conversation_by_id(db, conversation_id)
    if conversation:
        conversation.updated_at = updated_at or datetime.now(timezone.utc)
        db.commit()
        db.refresh(conversation)
    return conversation


def delete_conversation(db: Session, conversation_id: int) -> bool:
    """Konuşmayı siler (cascade ile mesajlar da silinir)."""
    conversation = get_conversation_by_id(db, conversation_id)
    if conversation:
        db.delete(conversation)
        db.commit()
        return True
    return False


# Message CRUD Operations
def create_message(db: Session, conversation_id: int, role: str, content: str) -> Optional[Message]:  # Optional ekle
    """Yeni mesaj oluşturur."""
    # Validasyonlar
    if role not in ["user", "assistant"]:
        return None

    conversation = get_conversation_by_id(db, conversation_id)
    if not conversation:
        return None

    db_message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message_by_id(db: Session, message_id: int) -> Optional[Message]:
    """ID'ye göre mesaj getirir."""
    return db.query(Message).filter(Message.id == message_id).first()


def get_messages_by_conversation(db: Session, conversation_id: int) -> list[type[Message]]:  # list[type[Message]] -> list[Message]
    """Konuşmanın tüm mesajlarını getirir."""
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc()).all()


def delete_message(db: Session, message_id: int) -> bool:
    """Mesajı siler."""
    message = get_message_by_id(db, message_id)
    if message:
        db.delete(message)
        db.commit()
        return True
    return False


def get_conversation_with_messages(db: Session, conversation_id: int) -> Optional[Conversation]:
    """Konuşmayı mesajlarıyla birlikte getirir."""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()
