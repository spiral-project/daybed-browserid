import os
import socket

from couchdb.client import Server
from couchdb.http import PreconditionFailed
from couchdb.design import ViewDefinition

from daybed import logger
from .views import docs

from . import views
from ..exceptions import UserIdNotFound, UserIdAlreadyExist


class CouchDBBackendConnectionError(Exception):
    pass


class CouchDBBackend(object):

    @classmethod
    def load_from_config(cls, config):
        settings = config.registry.settings
        return CouchDBBackend(
            host=settings['backend.db_host'],
            db_name=os.environ.get('DB_NAME', settings['backend.db_name']),
        )

    def __init__(self, host, db_name, id_generator):
        self.server = Server(host)
        self.db_name = db_name

        try:
            self.create_db_if_not_exist()
        except socket.error as e:
            raise CouchDBBackendConnectionError(
                "Unable to connect to the CouchDB server: %s - %s" % (host, e))

        self._db = self.server[self.db_name]
        self.sync_views()

    def delete_db(self):
        del self.server[self.db_name]

    def create_db_if_not_exist(self):
        try:
            self.server.create(self.db_name)
            logger.info('Creating and using db "%s"' % self.db_name)
        except PreconditionFailed:
            logger.info('Using db "%s".' % self.db_name)

    def sync_views(self):
        ViewDefinition.sync_many(self.server[self.db_name], docs)

    def __get_raw_user_token(self, user_id):
        try:
            return views.usertokens(self._db, key=user_id).rows[0].value
        except IndexError:
            raise UserIdNotFound(user_id)

    def get_user_token(self, user_id):
        """Returns the information associated with a user token"""
        usertoken = dict(**self.__get_raw_user_token(user_id))
        return usertoken['token']

    def add_token(self, user_id, token):
        # Check that the token doesn't already exist.
        try:
            self.__get_raw_user_token(user_id)
            raise UserIdAlreadyExist(user_id)
        except UserIdNotFound:
            pass

        doc = dict(token=token, user_id=user_id, type='usertoken')
        self._db.save(doc)
