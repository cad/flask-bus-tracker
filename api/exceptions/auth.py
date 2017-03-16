class AuthError(Exception):
    pass


class AuthCredentialsInvalid(AuthError):
    pass


class AuthHeaderMissing(AuthError):
    pass


class AuthHeaderMalformed(AuthError):
    pass


class AuthTokenMissing(AuthError):
    pass
