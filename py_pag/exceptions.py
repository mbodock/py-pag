class PagSeguroException(Exception):
    pass


class UnauthorizedException(PagSeguroException):
    pass


class NotificationNotFoundException(PagSeguroException):
    pass


class ApiErrorException(PagSeguroException):
    pass
