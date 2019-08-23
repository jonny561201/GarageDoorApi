from sqlalchemy import orm, create_engine

from svc.db.models.user_models import UserCredentials


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

    def are_credentials_valid(self, user, pword):
        user = self.session.query(UserCredentials).filter_by(user_name=user).first()
        return False if user is None else user.password == pword
