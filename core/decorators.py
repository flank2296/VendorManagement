from django.conf import settings
from django.http.response import HttpResponseForbidden


def authenticate_superuser(func_name):
    def wrapper(request, *args, **kwargs):
        # ToDo - Ankush Remove debug check
        if not request.user.is_superuser and not settings.DEBUG:
            return HttpResponseForbidden("Invalid user / user has logged out")

        return func_name(request, *args, **kwargs)

    return wrapper
