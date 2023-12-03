from django.db import models

from core.models import CoreModel, Vendor


class HistoricalPerformance(CoreModel):
    """Model which holds vendors historical Perofmatnce"""

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"

    class Meta:
        indexes = [
            models.Index(fields=["date"]),
        ]
        db_table = "HistoricalPerformance"
