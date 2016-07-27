class ClientException(Exception):
    pass


class AccessException(ClientException):
    def __init__(self, *args, **kwargs):
        super(AccessException).__init__(*args, **kwargs)