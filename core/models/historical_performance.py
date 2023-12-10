from django.db import models

from core.models.core import CoreModel
from core.models.vendor import Vendor


class HistoricalPerformance(CoreModel):
    """Model which holds vendors historical Performance"""

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    INSTANCE_LOOKUP_KEY = "vendor_id"

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"

    @classmethod
    def get_model_serializer(cls):
        from core.serializers.historical_performance import (
            HistoricalPerformanceSerializer,
        )

        return HistoricalPerformanceSerializer

    class Meta:
        indexes = [
            models.Index(fields=["date"]),
        ]
        db_table = "HistoricalPerformance"
