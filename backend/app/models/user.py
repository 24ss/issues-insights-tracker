from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "ADMIN"
    maintainer = "MAINTAINER"
    reporter = "REPORTER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.reporter.value)
