import traceback
from copy import deepcopy

from django.conf import settings
from django.http import HttpResponseServerError, JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from core.decorators import authenticate_superuser


@method_decorator(authenticate_superuser, name="dispatch")
class GenericView(APIView):
    """Basic Generic view used for CRUD. Expects a model in the URL pattern"""

    model = None

    def get(self, request, instance_id=None, *args, **kwargs):
        if not self.model:
            raise Exception("Invalid model name passed in the URL!")

        filters = deepcopy(self.model.INSTANCE_FETCHING_FILTERES)
        instance_id and filters.update(
            {f"{self.model.INSTANCE_LOOKUP_KEY}__in": [instance_id]}
        )
        instances = self.model.objects.filter(**filters).prefetch_related(
            *self.model.INSTANCE_FETCHING_PREFETCH_FIELD
        )
        return JsonResponse(
            {"instances": self.model.get_model_serializer()(instances, many=True).data}
        )

    def post(self, request, *args, **kwargs):
        """Generic insert view. Expects a model in the URL"""
        try:
            if not self.model:
                raise Exception("Invalid model name passed in the URL!")

            [
                kwargs.pop(key, None)
                for key in self.model.FIELDS_TO_IGNORE_WHILE_CREATION
            ]
            instance = self.model(**kwargs)
            instance.save()
            return JsonResponse(
                {"instance": self.model.get_model_serializer()(instance).data}
            )
        except:
            settings.DEBUG and traceback.print_exc()
            return HttpResponseServerError("Some exception occured!")

    def put(self, request, instance_id, *args, **kwargs):
        """Generic put view. Expects a instance id in the URL pattern"""
        try:
            if not instance_id:
                raise Exception("Invalid instance id passed for updating!")
            if not self.model:
                raise Exception("Invalid model name passed in the URL!")

            try:
                instance = self.model.objects.get(pk=instance_id)
            except:
                return HttpResponseServerError("Instance does not exists!")

            [setattr(instance, key, val) for key, val in kwargs.items()]
            instance.save()
            return JsonResponse(
                {"instance": self.model.get_model_serializer()(instance).data}
            )
        except:
            settings.DEBUG and traceback.print_exc()
            return HttpResponseServerError("Some error occured")
