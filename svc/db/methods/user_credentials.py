from sqlalchemy import orm, create_engine
from werkzeug.exceptions import BadRequest

from svc.db.models.user_information_model import UserPreference
from svc.db.models.user_login import UserCredentials


class UserDatabaseManager:
    db_session = None

    def __enter__(self):
        connection = 'postgres://postgres:password@localhost:5432/garage_door'

        db_engine = create_engine(connection)
        session = orm.sessionmaker(bind=db_engine)
        self.db_session = orm.scoped_session(session)

        return UserDatabase(self.db_session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.commit()
        self.db_session.remove()


class UserDatabase:
    def __init__(self, session):
        self.session = session

    #TODO: move throw down here and return user id
    def are_credentials_valid(self, user, pword):
        user = self.session.query(UserCredentials).filter_by(user_name=user).first()
        return False if user is None else user.password == pword

    def get_preferences_by_user(self, user_id):
        preference = self.session.query(UserPreference).filter_by(user_id=user_id).first()
        if preference is None:
            raise BadRequest
        return preference
