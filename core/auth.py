import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.http.response import HttpResponseForbidden
from django.middleware.csrf import rotate_token
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import authenticate_superuser


def ping(request):
    rotate_token(request)
    return JsonResponse({"message": "pong"})


class UserLogin(View):
    """loggs in a user if user is authenticated"""

    def post(self, request, *args, **kwargs):
        """Validated a user based on username and password and logs in"""
        payload = json.loads(request.body)
        username = payload.get("username")
        password = payload.get("password")

        if not any([username, password]):
            return HttpResponseForbidden("Invalid user credentials")

        user = authenticate(username=username, password=password)
        if not user or not user.is_authenticated:
            return HttpResponseForbidden("Invalid user credentials")

        login(request, user)
        # ToDo - Add session variables here
        return JsonResponse({"message": "user logged in successfully"})


@method_decorator(authenticate_superuser, name="dispatch")
class UserLogout(View):
    """Logs out an user from the system"""

    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"message": "logout successful!"})
