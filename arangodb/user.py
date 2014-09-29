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

        user_name = user['user']
        change_password = user['changePassword']
        active = user['active']
        extra = user['extra']

        user_obj = cls(name=user_name, change_password=change_password, active=active, extra=extra, api=api)

        return user_obj

    @classmethod
    def create(cls, name, password='', active=True, extra=None, change_password=False):
        """
        """

        api = Client.instance().api

        api.user.post({
            'user': name,
            'passwd': password,
            'active': active,
            'exta': extra,
            'changePassword': change_password,
        })

        user_obj = cls(name=name, change_password=change_password, active=active, extra=extra, api=api)

        return user_obj

    @classmethod
    def remove(cls, name):
        """
        """

        api = Client.instance().api

        api.user(name).delete()


    def __init__(self, name, change_password, active, api, extra=None):
        """
        """

        self.name = name
        self.change_password = change_password
        self.active = active
        self.extra = extra

        self.api = api


