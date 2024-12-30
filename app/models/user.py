from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username chosen by the user.
        email (str): Email address of the user.
        password (str): Password for the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.

    Relationships:
        profile (UserProfile): The user's profile.
    """
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone.utc)
    )

    # Relationship
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    budgets = relationship("Budget", back_populates="user")


class UserProfile(Base):
    """
    Represents a user's profile in the system.

    Attributes:
        id (int): Unique identifier for the user's profile.
        user_id (int): Foreign key referencing the User table.
        first_name (str): User's first name.
        last_name (str): User's last name.
        avatar (str): URL or file path to the user's profile picture.
        created_at (datetime): Timestamp when the user's profile was created.
        updated_at (datetime): Timestamp when the user's profile was last updated.

    Relationships:
        user (User): The user who owns this profile.
    """
    __tablename__ = "User_Profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone.utc)
    )

    # Relationship
    user = relationship("User", back_populates="profile")