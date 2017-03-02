from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import database.services as db_services

class SumoDB(object):

    def __init__(self, uri, metadata=None, engine_options=None, session_options=None, scopefunc=None, services=None):
        engine_options = engine_options or {}
        session_options = session_options or {}

        self.uri = uri

        self._engine = create_engine(self.uri, **engine_options)
        self._session = scoped_session(sessionmaker(bind=self.engine, **session_options), scopefunc=scopefunc)

        self.Model = declarative_base(metadata=metadata)
        self.metadata.bind = self.engine
        
        self._services = None
        self._register_services(services=services)        

    @property
    def metadata(self):
        return self.Model.metadata

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

    @property
    def query(self):
        return self.session.query

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def drop_all(self):
        self.metadata.drop_all()
    
    def create_all(self):
        self.metadata.create_all()

    def _register_services(self, services=None):
        if self._services is None:
            self._services = services or db_services.init(self)
        return self._services

    @property
    def services(self):
        return self._services
