import functools
from enum import Enum, unique
from collections import Iterable

from flask import Blueprint, jsonify, Response, abort

api = Blueprint('api', __name__)


@unique
class Error(Enum):
    # tuple(error code, default error message, default status code)
    UNDEFINED = (100, 'Undefined error.', 400)
    NO_SUCH_API = (101, 'No such API.', 404)
    RESOURCE_NOT_EXISTS = (102, 'The resource does not exist.', 404)
    INVALID_ARGUMENTS = (103, 'Invalid argument(s).', 400)
    NOT_ALLOWED = (104, 'The resource path is not allowed.', 403)
    BAD_PATH = (105, 'The resource path cannot be recognized.', 400)


class ApiException(Exception):
    def __init__(self, message=None, error=Error.UNDEFINED, status_code=None, payload=None):
        super(ApiException, self).__init__()
        self.message = message
        self.status_code = status_code
        self.error = error
        self.payload = payload

    def to_dict(self):
        result = dict(self.payload or {})
        result['code'] = self.error.value[0]
        result['message'] = self.message or self.error.value[1]
        return result


@api.errorhandler(ApiException)
def handle_api_exception(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code or e.error.value[2]
    return response


def json_api(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise ApiException(error=Error.RESOURCE_NOT_EXISTS)

        if isinstance(result, Response):
            return result

        try:
            return jsonify(result)
        except TypeError as e:
            if isinstance(result, Iterable):
                return jsonify(list(result))
            else:
                raise e

    return wrapper


from veripress.api import handlers

from veripress.helpers import url_rule
rule = functools.partial(url_rule, api, strict_slashes=False)

rule('/site', endpoint='site', view_func=handlers.site_info, methods=['GET'])
rule(['/posts',
      '/posts/<int:year>',
      '/posts/<int:year>/<int:month>',
      '/posts/<int:year>/<int:month>/<int:day>',
      '/posts/<int:year>/<int:month>/<int:day>/<string:post_name>'], view_func=handlers.posts, methods=['GET'])
rule('/tags', view_func=handlers.tags, methods=['GET'])
rule('/categories', view_func=handlers.categories, methods=['GET'])
rule('/widgets', view_func=handlers.widgets, methods=['GET'])
rule('/custom_pages/<path:page_path>', view_func=handlers.custom_pages, methods=['GET'], strict_slashes=True)
rule('/search', view_func=handlers.search, methods=['GET'])

rule('/<path:_>', view_func=lambda _: abort(404), methods=['GET', 'POST'])  # direct unknown path to 404


@api.errorhandler(404)
def handle_page_not_found(e):
    return handle_api_exception(ApiException(error=Error.NO_SUCH_API))