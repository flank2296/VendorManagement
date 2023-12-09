from django.db import models

# Create your models here.


class CoreModel(models.Model):
    """Core model which adds basic utilites to a model"""

    INSTANCE_FETCHING_FILTERES = {}
    FIELDS_TO_IGNORE_WHILE_CREATION = ["pk", "created_at", "updated_at"]

    INSTANCE_FETCHING_PREFETCH_FIELD = []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def get_model_serializer(cls):
        return None

    @property
    def is_new(self):
        """Checks if the instance is new or already created"""
        return bool(self.pk)

    def validate(self, *args, **kwargs):
        """Extend this method in model to add validations"""
        return

    def before_save(self, *args, **kwargs):
        """Extend this method in model to add before save actions"""
        return

    def after_save(self, *args, **kwargs):
        """Extend this method in model to add after save actions"""
        return

    def save(self, *args, **kwargs) -> None:
        """Overrides core django model's save method to add before and after save methods"""
        self.validate(*args, **kwargs)
        self.before_save(*args, **kwargs)
        super().save(*args, **kwargs)
        self.after_save(*args, **kwargs)
