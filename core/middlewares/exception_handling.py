import traceback

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class ExceptionHandlingMiddleware(MiddlewareMixin):
    """A custom exception handling middleware. Handles all api responses"""

    def process_exception(self, request, exception):
        response = {"message": "Some error occured!"}
        if settings.DEBUG:
            traceback.print_exc()
            response.update({"traceback": traceback.format_exc()})

        return JsonResponse(response, status=500)
