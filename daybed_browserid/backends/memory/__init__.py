from copy import deepcopy

from ..exceptions import UserIdNotFound, UserIdAlreadyExist


class MemoryBackend(object):

    @classmethod
    def load_from_config(cls, config):
        return MemoryBackend()

    def __init__(self):
        self._init_db()

    def delete_db(self):
        self._db.clear()
        self._init_db()

    def _init_db(self):
        self._db = {
            'usertokens': {}
        }

    def get_user_token(self, user_id):
        """Retrieves a token for the userid"""
        try:
            return str(self._db['usertokens'][user_id])
        except KeyError:
            raise UserIdNotFound(user_id)

    def store_user_token(self, user_id, token):
        # Check that the token doesn't already exist.
        # Check that the token doesn't already exist.
        try:
            self.get_user_token(user_id)
            raise UserIdAlreadyExist(user_id)
        except UserIdNotFound:
            pass

        self._db['usertokens'][user_id] = token
