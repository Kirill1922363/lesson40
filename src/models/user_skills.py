
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.orm import relationship
from settings import Base
import enum


class ExchangeStatus(enum.Enum):
    """Статуси обміну навичками"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User(Base):
    """Модель користувача платформи"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    
    avatar_url = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    skills_offered = relationship("Skill", back_populates="user", foreign_keys="Skill.user_id")
    exchanges_initiated = relationship(
        "Exchange", 
        back_populates="initiator", 
        foreign_keys="Exchange.initiator_id"
    )
    exchanges_received = relationship(
        "Exchange", 
        back_populates="receiver", 
        foreign_keys="Exchange.receiver_id"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Category(Base):
    """Модель категорії навичок (Завдання 4)"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)

    skills = relationship("Skill", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Skill(Base):
    """Модель навички"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    level = Column(String(20), nullable=False)  
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    is_offered = Column(Boolean, default=True)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="skills_offered")
    category = relationship("Category", back_populates="skills")

    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', level='{self.level}')>"


class Exchange(Base):
    """Модель обміну навичками між користувачами"""
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True)
    initiator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    skill_offered_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    skill_requested_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(
        Enum(ExchangeStatus), 
        default=ExchangeStatus.PENDING, 
        nullable=False,
        index=True
    )
    message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Зв'язки
    initiator = relationship("User", back_populates="exchanges_initiated", foreign_keys=[initiator_id])
    receiver = relationship("User", back_populates="exchanges_received", foreign_keys=[receiver_id])
    skill_offered = relationship("Skill", foreign_keys=[skill_offered_id])
    skill_requested = relationship("Skill", foreign_keys=[skill_requested_id])

    def __repr__(self):
        return f"<Exchange(id={self.id}, status='{self.status.value}')>"