from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime, timezone

# Association Table for Many-to-Many: Users <-> Interests
class UserInterests(Base):
    __tablename__ = 'user_interests'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    interest_id = Column(Integer, ForeignKey('interests.id'), primary_key=True)

# Association Table for Encounters (symmetric relationship)
class Encounter(Base):
    __tablename__ = 'encounter'
    user_id_1 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id_2 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# Association Table for Friendships (symmetric relationship)
class Friendship(Base):
    __tablename__ = 'friendships'
    user_id_1 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id_2 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# Association Table for Blocked Users
class Blocked(Base):
    __tablename__ = 'blocked'
    blocker_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    blocked_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    location = Column(String)
    # Coordinates do not live here
    gender = Column(String)
    religion = Column(String)
    race = Column(String)
    bio = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    interests = relationship('Interest', secondary='user_interests', back_populates='users')
    shared_thoughts = relationship('SharedThought', back_populates='user')
    searches = relationship('Search', back_populates='user')
    events = relationship('Event', back_populates='creator')
    votes = relationship('Vote', back_populates='user')

class Interest(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(Integer)

    # Reverse relationship
    users = relationship('User', secondary='user_interests', back_populates='interests')

class SharedThought(Base):
    __tablename__ = 'shared_thoughts'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship('User', back_populates='shared_thoughts')

class Search(Base):
    __tablename__ = 'search'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='searches')

class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    location = Column(String)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    description = Column(String)

    events = relationship('Event', back_populates='place')
    votes = relationship('Vote', back_populates='place')

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    description = Column(String)
    place_id = Column(Integer, ForeignKey('places.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    event_date_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    place = relationship('Place', back_populates='events')
    creator = relationship('User', back_populates='events')

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    up_down = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    type = Column(String)

    user = relationship('User', back_populates='votes')
    place = relationship('Place', back_populates='votes')