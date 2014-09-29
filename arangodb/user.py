from arangodb.api import Client


class User(object):
    """
    """

    @classmethod
    def get(cls, name):
        """
        """

        api = Client.instance().api

        user = api.user(name).get()

        change_password = user['changePassword']
        active = user['active']
        extra = user['extra']

        user_obj = cls(name=name, change_password=change_password, active=active, extra=extra, api=api)

        return user_obj

    def __init__(self, name, change_password, active, api, extra=None):
        """
        """

        self.name = name
        self.change_password = change_password
        self.active = active
        self.extra = extra

        self.name = api