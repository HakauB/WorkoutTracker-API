import imp
import json
from urllib import response
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from settings import JWT_REFRESH_COOKIE


class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # TODO: Set to actual path
        if request.path == 'token/refresh/' and JWT_REFRESH_COOKIE in request.COOKIES:

            if request.body != b'':
                data = json.loads(request.body)
                data['refresh'] = request.COOKIES[JWT_REFRESH_COOKIE]
                request._body = json.dumps(data).encode('utf-8')
            # TODO: Else: Log error
            else:
                pass
        return None
