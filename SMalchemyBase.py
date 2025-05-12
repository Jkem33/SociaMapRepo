#DLL/Schema
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone


# Base class used to define models (tables)
Base = declarative_base()


# Interests Table
class Interest(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    users = relationship("UserInterests", back_populates="interest")

   
# Associaiton Table, UserIntresests Table 
class UserInterests(Base):
    __tablename__ = 'user_interests'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    interest_id = Column(Integer, ForeignKey('interests.id'), primary_key=True)

    user = relationship("User", back_populates="user_interests")
    interest = relationship("Interest", back_populates="users")

  
# Places table
class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    location = Column(String)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    description = Column(String)

    votes = relationship("Vote", back_populates="place")
    events = relationship("Event", back_populates="place")

# Events table
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

    place = relationship("Place", back_populates="events")
    creator = relationship("User", back_populates="events")

# Search table
class Search(Base):
    __tablename__ = 'search'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="searches")

# Shared Thoughts table
class SharedThought(Base):
    __tablename__ = 'shared_thoughts'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="shared_thoughts")

# Votes table
class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    up_down = Column(Boolean) #trye for upvote, false for downvote
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))

    user = relationship("User", back_populates="votes")
    place = relationship("Place", back_populates="votes")

# Friendships table
class Friendship(Base):
    __tablename__ = 'friendships'
    user_id1 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id2 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# Encounter table
class Encounter(Base):
    __tablename__ = 'encounter'
    user_id1 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id2 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    
# Blocked table
class Blocked(Base):
    __tablename__ = 'blocked'
    blocker_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    blocked_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    blocker_user = relationship("User", back_populates="blocked", foreign_keys=[blocker_id])
    blocked_user = relationship("User", back_populates="blocked_by", foreign_keys=[blocked_id])

# Users Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    location = Column(String)
    gender = Column(String)
    religion = Column(String)
    race = Column(String)
    bio = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    # the relationship with users
    votes = relationship("Vote", back_populates= "user")
    searches = relationship("Search", back_populates= "user")
    shared_thoughts = relationship("SharedThought", back_populates="user")
    user_interests = relationship("UserInterests", back_populates="user")
    events = relationship("Event", back_populates="creator")
    
    #i used AI for this because it mentioned "You have multiple relationships in the User model that involve the same underlying table (blocked) and column (users.id)"
    blocked = relationship("Blocked", foreign_keys=[Blocked.blocker_id], back_populates="blocker_user")
    blocked_by = relationship("Blocked", foreign_keys=[Blocked.blocked_id], back_populates='blocked_user', overlaps="blocked,blocker_user") 

    encounters = relationship("Encounter", foreign_keys=[Encounter.user_id1], backref="user1")
    encountered_by = relationship("Encounter", foreign_keys=[Encounter.user_id2], backref="user2")
    
    friendship = relationship("Friendship", foreign_keys=[Friendship.user_id1], backref="user1")
    friendship_by = relationship("Friendship", foreign_keys=[Friendship.user_id2], backref="user2")
