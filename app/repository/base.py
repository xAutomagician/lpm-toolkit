"""
BASE REPOSITORY
"""


class Repository:
    def create(self, data):
        raise NotImplementedError

    def read(self, id):
        raise NotImplementedError

    def update(self, id, data):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError
