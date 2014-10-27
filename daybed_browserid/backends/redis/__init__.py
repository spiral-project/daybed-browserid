# -*- coding: utf-8 -*-
import redis

from ..exceptions import UserIdNotFound, UserIdAlreadyExist


class RedisBackend(object):

    @classmethod
    def load_from_config(cls, config):
        settings = config.registry.settings

        return RedisBackend(
            settings.get('backend.db_host', 'localhost'),
            settings.get('backend.db_port', 6379),
            settings.get('backend.db_index', 0)
        )

    def __init__(self, host, port, db):
        self._db = redis.StrictRedis(host=host, port=port, db=db)

        # Ping the server to be sure the connection works.
        self._db.ping()

    def delete_db(self):
        self._db.flushdb()

    def get_user_token(self, user_id):
        """Retrieves a token for the userid"""
        token = self._db.get("usertoken.%s" % user_id)
        if token is None:
            raise UserIdNotFound(user_id)
        return token.decode("utf-8")

    def store_user_token(self, user_id, token):
        # Check that the token doesn't already exist.
        try:
            self.get_user_token(user_id)
            raise UserIdAlreadyExist(user_id)
        except UserIdNotFound:
            pass

        self._db.set("usertoken.%s" % user_id, token)
