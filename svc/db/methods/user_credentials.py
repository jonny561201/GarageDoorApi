import os
from sqlalchemy import orm, create_engine


class UserDatabaseManager(object):
    def __init__(self):
        self.db_session = None

    def __enter__(self):
        db_conn_string = '{0}://{1}:{2}@{3}:{4}/{5}'.format(os.environ["DB_TYPE"],
                                                            os.environ["DB_USER"],
                                                            os.environ["DB_PASS"],
                                                            os.environ["DB_HOST"],
                                                            os.environ["DB_PORT"],
                                                            os.environ["DB_NAME"])

        db_engine = create_engine(db_conn_string)
        self.db_session = orm.scoped_session(orm.sessionmaker(bind=db_engine))

        return UserDatabase(self.db_session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.commit()
        self.db_session.remove()


class UserDatabase(object):
    def __init__(self, session):
        super(UserDatabase, self).__init__()
        self.session = session

    def user_credentials_are_valid(self):
        pass
