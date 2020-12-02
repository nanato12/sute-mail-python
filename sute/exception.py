class LoginFailed(Exception):
    """
    login failed exception.
    """


class GetAccountInfoError(Exception):
    """
    get account information exception.
    """


class AlreadyEmailAddressExsist(Exception):
    """
    when a new email address already exists.
    """


class ReadTimeoutError(Exception):
    """
    request session connection timeout exception.
    """


class ConnectionTimeoutError(Exception):
    """
    request session connection timeout exception.
    """


class ParseError(Exception):
    """
    Scraping parse exception.
    """


class UnknownException(Exception):
    """
    unknown exception.
    """
