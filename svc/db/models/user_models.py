from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext import declarative

Base = declarative.declarative_base()


class UserCredentials(Base):
    __table_args__ = ({'schema': 'user_credentials'})
    __tablename__ = 'users'
    user_key = Column(UUID, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
