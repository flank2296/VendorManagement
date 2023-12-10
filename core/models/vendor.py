from django.db import models

from core.models.core import CoreModel


class Vendor(CoreModel):
    """Model which holds vendor's meta"""

    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)
    is_disabled = models.BooleanField(default=False)

    INSTANCE_FETCHING_FILTERES = {"is_disabled": False}

    @classmethod
    def get_model_serializer(cls):
        from core.serializers.vendor import VendorSerializer

        return VendorSerializer

    def __str__(self):
        return f"{self.name}"

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["vendor_code"]),
        ]
        db_table = "Vendor"
