import json
from copy import deepcopy

from rest_framework.views import APIView

from django.http import JsonResponse
from django.utils.decorators import method_decorator

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
        payload = json.loads(request.body)
        if not self.model:
            raise Exception("Invalid model name passed in the URL!")

        [payload.pop(key, None) for key in self.model.FIELDS_TO_IGNORE_WHILE_CREATION]
        instance = self.model(**payload)
        instance.save()
        return JsonResponse(
            {"instance": self.model.get_model_serializer()(instance).data}
        )

    def put(self, request, instance_id, *args, **kwargs):
        """Generic put view. Expects a instance id in the URL pattern"""
        payload = json.loads(request.body)

        if not instance_id:
            raise Exception("Invalid instance id passed for updating!")
        if not self.model:
            raise Exception("Invalid model name passed in the URL!")

        instance = self.model.objects.get(pk=instance_id)
        [setattr(instance, key, val) for key, val in payload.items()]
        instance.save()
        return JsonResponse(
            {"instance": self.model.get_model_serializer()(instance).data}
        )

    def delete(self, request, instance_id, *args, **kwargs):
        """Generic Delete action on model level"""
        if not instance_id:
            raise Exception("Invalid instance id passed for updating!")
        if not self.model:
            raise Exception("Invalid model name passed in the URL!")

        self.model.objects.filter(pk=instance_id).delete()
        return JsonResponse({"message": "successfully deleted!"})
