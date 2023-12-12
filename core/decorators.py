from django.http.response import HttpResponseForbidden


def authenticate_superuser(func_name):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Invalid user / user has logged out")

        return func_name(request, *args, **kwargs)

    return wrapper
