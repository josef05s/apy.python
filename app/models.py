from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True,nullable=True)
    title = Column(String,nullable=True)
    content = Column(String,nullable=True)
    published = Column(Boolean, server_default='True' , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
     __tablename__ = "users"
     id = Column(Integer, primary_key=True,nullable=True)
     email = Column(String,nullable=True,unique=True)
     password = Column(String,nullable=True)
     created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))    