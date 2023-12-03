from django.db import models

from core.models import Vendor, CoreModel


class PurchaseOrder(CoreModel):
    """Model which holds vendors PO meta"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"

    class Meta:
        indexes = [
            models.Index(fields=["po_number"]),
            models.Index(fields=["order_date"]),
            models.Index(fields=["delivery_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["issue_date"]),
            models.Index(fields=["acknowledgment_date"]),
        ]
        db_table = "PurchaseOrder"
