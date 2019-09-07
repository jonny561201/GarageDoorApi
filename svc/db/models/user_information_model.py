from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship

Base = declarative.declarative_base()


class UserInformation(Base):
    __tablename__ = 'user_information'

    id = Column(UUID, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)


class UserPreference(Base):
    __tablename__ = 'user_preferences'

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(UUID, ForeignKey(UserInformation.id))
    is_fahrenheit = Column(Boolean, nullable=False)

    user = relationship('UserInformation', foreign_keys='UserPreference.user_id')


class UserCredentials(Base):
    __tablename__ = 'user_login'

    id = Column(UUID, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey(UserInformation.id))

    user = relationship('UserInformation', foreign_keys='UserCredentials.user_id')


class DailySumpPumpLevel(Base):
    __tablename__ = 'daily_sump_level'

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(UUID, ForeignKey(UserInformation.id))
    distance = Column(DECIMAL, nullable=False)
    create_date = Column(TIMESTAMP, nullable=False)

    user = relationship('UserInformation', foreign_keys='DailySumpPumpLevel.user_id')

