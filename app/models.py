import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# --------------------------
# Modèle pour les posts 
# -------------------------
class Post(Base):
    """
    Docstring for Post
    """
    __tablename__= "post" 

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True, comment="Unique identifier of the post")
    title = Column(String(200), nullable=False, comment="Title of the post")
    content = Column(String, nullable=False, comment="Content of the post")
    published = Column(Boolean, default=True, nullable=False, comment="Publication status of the post")
    rating = Column(Integer, nullable=True, comment="Rating of the post")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id  = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="Identifier of the user who created the post")


    owner = relationship("User", back_populates="posts")

# --------------------------
# Modèle pour les utilisateurs  
# --------------------------
class User(Base):
    """
    Docstring for User
    """
    __tablename__= "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False, comment="Unique identifier of the user")
    email = Column(String, unique=True, nullable=False, index=True, comment="Email address of the user")
    password = Column(String, nullable=False, comment="Hashed password of the user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("Post", back_populates="owner", lazy="select", cascade="all, delete-orphan")

# --------------------------
# Modèle pour les votes
# --------------------------
class Vote(Base):
    """
    Docstring for Vote
    """
    __tablename__= "votes"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False, comment="Identifier of the user who voted")
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True, nullable=False, comment="Identifier of the post that was voted on")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))