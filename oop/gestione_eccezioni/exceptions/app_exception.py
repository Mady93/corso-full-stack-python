# -----------------------------------------------------------------------------
# HTTP EXCEPTION HIERARCHY (FOR FUTURE API / HTTP EXTENSION)
# -----------------------------------------------------------------------------
# These classes map standard domain exceptions to HTTP Status codes using Python's
# `http.HTTPStatus`. They are currently disabled for CLI execution, but ready to 
# be decommented when migrating the core business logic to a Web API framework 
# (e.g., FastAPI, Flask, or Django).
# ====

# from http import HTTPStatus


# class AppException(Exception):
#     """Base exception for application-specific errors"""

#     status = HTTPStatus.INTERNAL_SERVER_ERROR


# class BadRequestException(AppException):
#     """Raised when the request is malformed or invalid"""

#     status = HTTPStatus.BAD_REQUEST


# class UnauthorizedException(AppException):
#     """Raised when authentication is required"""

#     status = HTTPStatus.UNAUTHORIZED


# class ForbiddenException(AppException):
#     """Raised when access is denied"""

#     status = HTTPStatus.FORBIDDEN


# class NotFoundException(AppException):
#     """Raised when the requested resource does not exist"""

#     status = HTTPStatus.NOT_FOUND


# class MethodNotAllowedException(AppException):
#     """Raised when the HTTP method is not allowed"""

#     status = HTTPStatus.METHOD_NOT_ALLOWED


# class NotAcceptableException(AppException):
#     """Raised when the requested representation is not acceptable"""

#     status = HTTPStatus.NOT_ACCEPTABLE


# class RequestTimeoutException(AppException):
#     """Raised when the request times out"""

#     status = HTTPStatus.REQUEST_TIMEOUT


# class ConflictException(AppException):
#     """Raised when the request conflicts with the current state"""

#     status = HTTPStatus.CONFLICT


# class GoneException(AppException):
#     """Raised when the requested resource is no longer available"""

#     status = HTTPStatus.GONE


# class PreconditionFailedException(AppException):
#     """Raised when a request precondition is not satisfied"""

#     status = HTTPStatus.PRECONDITION_FAILED


# class ContentTooLargeException(AppException):
#     """Raised when the request content is too large"""

#     status = HTTPStatus.CONTENT_TOO_LARGE


# class UnsupportedMediaTypeException(AppException):
#     """Raised when the media type is not supported"""

#     status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE


# class UnprocessableContentException(AppException):
#     """Raised when the content is semantically invalid"""

#     status = HTTPStatus.UNPROCESSABLE_CONTENT


# class TooManyRequestsException(AppException):
#     """Raised when too many requests have been sent"""

#     status = HTTPStatus.TOO_MANY_REQUESTS


# class NotImplementedException(AppException):
#     """Raised when the requested functionality is not implemented"""

#     status = HTTPStatus.NOT_IMPLEMENTED


# class BadGatewayException(AppException):
#     """Raised when an upstream server returns an invalid response"""

#     status = HTTPStatus.BAD_GATEWAY


# class ServiceUnavailableException(AppException):
#     """Raised when the service is temporarily unavailable"""

#     status = HTTPStatus.SERVICE_UNAVAILABLE


# class GatewayTimeoutException(AppException):
#     """Raised when an upstream server does not respond in time"""

#     status = HTTPStatus.GATEWAY_TIMEOUT



class AppException(Exception):
    """Base exception for application-specific errors"""


class ValidationError(AppException):
    """Raised when application data is invalid"""


class NotFoundError(AppException):
    """Raised when a requested resource does not exist"""


class ConflictError(AppException):
    """Raised when an operation conflicts with the current state"""


class UnauthorizedError(AppException):
    """Raised when authentication is required"""


class ForbiddenError(AppException):
    """Raised when an operation is not permitted"""


class SaldoInsufficienteError(ConflictError):
    """Raised when the account balance is insufficient"""