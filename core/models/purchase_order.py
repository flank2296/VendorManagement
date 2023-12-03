from django.db import models

from core.models.vendor import Vendor
from core.models.core import CoreModel


class PurchaseOrder(CoreModel):
    """Model which holds vendors PO meta"""

    STATUS_PENDING = "Pending"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Canceled"
    VALID_STATUSES = [STATUS_CANCELLED, STATUS_COMPLETED, STATUS_PENDING]

    STATUS_CHOICES = [
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_COMPLETED, STATUS_COMPLETED),
        (STATUS_CANCELLED, STATUS_CANCELLED),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    _status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, db_column="status"
    )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    # Custom class attibutes used for manipulating functionalities
    is_status_changed = False
    is_acknowledging_now = False

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"

    @property
    def is_completed(self):
        """A property which tells if the current PO is completed or not"""
        return self.status == PurchaseOrder.STATUS_COMPLETED

    @property
    def status(self):
        """Getter for status"""
        return self._status

    @status.setter
    def status(self, status_to_update=""):
        """A setter function for changing status of a PO"""
        if status_to_update not in PurchaseOrder.VALID_STATUSES:
            raise ValueError("Invalid status option passed for updating")

        self.is_status_changed = self.status != status_to_update
        self._status = status_to_update

    def after_save(self, *args, **kwargs):
        """Overrides core models after save action to support actions"""
        if current_status := self.is_status_changed and self.is_completed:
            # ToDo - Ankush. Calculate on time delivery rate
            if current_status and self.quality_rating:
                # ToDo - Ankush. Calculate quality rating average
                pass
            pass

        if self.is_status_changed:
            # ToDo - Ankush. calculate fulfilment rate
            pass

        if self.is_acknowledging_now:
            # ToDo - Calculate average response time
            pass

    class Meta:
        indexes = [
            models.Index(fields=["po_number"]),
            models.Index(fields=["order_date"]),
            models.Index(fields=["delivery_date"]),
            models.Index(fields=["_status"]),
            models.Index(fields=["issue_date"]),
            models.Index(fields=["acknowledgment_date"]),
        ]
        db_table = "PurchaseOrder"
