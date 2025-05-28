from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_ngo = Column(Integer, default=0)  # 0 = volunteer, 1 = NGO

    ngo_profile = relationship("NGOProfile", back_populates="user", uselist=False)
    volunteer_profile = relationship("VolunteerProfile", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)


class NGOProfile(Base):
    __tablename__ = "ngo_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    user = relationship("User", back_populates="ngo_profile")
    opportunities = relationship("Opportunity", back_populates="ngo")


class VolunteerProfile(Base):
    __tablename__ = "volunteer_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String(100), nullable=False)
    bio = Column(Text)

    # Relação apenas para o usuário, sem citar aplicações aqui
    user = relationship("User", back_populates="volunteer_profile")


class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngo_profiles.id"))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    ngo = relationship("NGOProfile", back_populates="opportunities")
    applications = relationship("Application", back_populates="opportunity")


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    status = Column(String(20), default="pending")
    applied_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications")
