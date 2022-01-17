from typing import Optional

from flask import make_response

from main.schemas.exceptions import ErrorSchema


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class _ErrorCode:
    VALIDATION_ERROR = 400000
    ITEM_EXISTED = 400001
    CATEGORY_EXISTED = 400002
    EMAIL_EXISTED = 400003
    LOGIN_UNSUCCESSFULLY = 400006
    UNAUTHORIZED = 401000
    ITEM_UPDATE_FORBIDDEN = 403000
    ITEM_DELETE_FORBIDDEN = 403001
    CATEGORY_DELETE_FORBIDDEN = 403002
    NOT_FOUND = 404000
    ITEM_NOT_FOUND = 404001
    CATEGORY_NOT_FOUND = 404002
    METHOD_NOT_ALLOWED = 405000
    INTERNAL_SERVER_ERROR = 500000


class _ErrorMessage:
    VALIDATION_ERROR = "Validation error."
    ITEM_EXISTED = "Item existed."
    CATEGORY_EXISTED = "Category existed."
    EMAIL_EXISTED = "Email existed."
    LOGIN_UNSUCCESSFULLY = "Login unsuccessfully."
    UNAUTHORIZED = "Unauthorized."
    ITEM_UPDATE_FORBIDDEN = "Not allowed to update this item."
    ITEM_DELETE_FORBIDDEN = "Not allowed to delete this item."
    CATEGORY_DELETE_FORBIDDEN = "Not allowed to delete this category."
    NOT_FOUND = "Not found."
    ITEM_NOT_FOUND = "Item not found."
    CATEGORY_NOT_FOUND = "Category not found."
    METHOD_NOT_ALLOWED = "Method not allowed."
    INTERNAL_SERVER_ERROR = "Internal server error."


class BaseError(Exception):
    def __init__(
        self,
        *,
        error_message=None,
        error_data=None,
        status_code: Optional[int] = None,
        error_code: Optional[int] = None,
    ):
        """
        Customize the response exception

        :param error_message: <string> Message field in the response body
        :param status_code: <number> HTTP status code
        :param error_data: <dict> Json body data
        :param error_code: <number> error code
        """
        if error_message is not None:
            self.error_message = error_message

        if status_code is not None:
            self.status_code = status_code

        if error_code is not None:
            self.error_code = error_code

        self.error_data = error_data

    def to_response(self):
        response = ErrorSchema().jsonify(self)

        return make_response(response, self.status_code)


class ValidationError(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.VALIDATION_ERROR
    error_code = _ErrorCode.VALIDATION_ERROR


class EmailExisted(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.EMAIL_EXISTED
    error_code = _ErrorCode.EMAIL_EXISTED


class ItemExisted(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.ITEM_EXISTED
    error_code = _ErrorCode.ITEM_EXISTED


class CategoryExisted(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.CATEGORY_EXISTED
    error_code = _ErrorCode.CATEGORY_EXISTED


class LoginUnsuccessfully(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.LOGIN_UNSUCCESSFULLY
    error_code = _ErrorCode.LOGIN_UNSUCCESSFULLY


class Unauthorized(BaseError):
    status_code = StatusCode.UNAUTHORIZED
    error_message = _ErrorMessage.UNAUTHORIZED
    error_code = _ErrorCode.UNAUTHORIZED


class ItemUpdateForbidden(BaseError):
    status_code = StatusCode.FORBIDDEN
    error_message = _ErrorMessage.ITEM_UPDATE_FORBIDDEN
    error_code = _ErrorCode.ITEM_UPDATE_FORBIDDEN


class ItemDeleteForbidden(BaseError):
    status_code = StatusCode.FORBIDDEN
    error_message = _ErrorMessage.ITEM_DELETE_FORBIDDEN
    error_code = _ErrorCode.ITEM_DELETE_FORBIDDEN


class CategoryDeleteForbidden(BaseError):
    status_code = StatusCode.FORBIDDEN
    error_message = _ErrorMessage.CATEGORY_DELETE_FORBIDDEN
    error_code = _ErrorCode.CATEGORY_DELETE_FORBIDDEN


class NotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.NOT_FOUND
    error_code = _ErrorCode.ITEM_NOT_FOUND


class ItemNotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.ITEM_NOT_FOUND
    error_code = _ErrorCode.ITEM_NOT_FOUND


class CategoryNotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.CATEGORY_NOT_FOUND
    error_code = _ErrorCode.CATEGORY_NOT_FOUND


class MethodNotAllowed(BaseError):
    status_code = StatusCode.METHOD_NOT_ALLOWED
    error_message = _ErrorMessage.METHOD_NOT_ALLOWED
    error_code = _ErrorCode.METHOD_NOT_ALLOWED


class InternalServerError(BaseError):
    status_code = StatusCode.INTERNAL_SERVER_ERROR
    error_message = _ErrorMessage.INTERNAL_SERVER_ERROR
    error_code = _ErrorCode.INTERNAL_SERVER_ERROR
