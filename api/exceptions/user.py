class UserError(Exception):
    pass


class UserNotFound(UserError):
    pass


class UserAlreadyExists(UserError):
    pass


class UserUnknownError(UserError):
    def __init__(self, errors):
        self.errors = errors
