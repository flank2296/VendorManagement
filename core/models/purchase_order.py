import math

from django.db import models
from django.utils import timezone

from core.models.core import CoreModel
from core.models.vendor import Vendor


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
    order_date = models.DateTimeField(auto_now_add=True)

    # Added 2 dates for delivery. Expected and actual
    delivery_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)

    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, db_column="status")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    # Custom class attibutes used for manipulating functionalities
    is_status_changed = False
    is_acknowledging_now = False

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"

    @classmethod
    def get_model_serializer(cls):
        from core.serializers.purchase_order import PurchaseOrdersSerializer

        return PurchaseOrdersSerializer

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["po_number"]),
            models.Index(fields=["issue_date"]),
            models.Index(fields=["order_date"]),
            models.Index(fields=["delivery_date"]),
            models.Index(fields=["acknowledgment_date"]),
            models.Index(fields=["expected_delivery_date"]),
        ]
        db_table = "PurchaseOrder"

    def before_save(self, *args, **kwargs):
        """Overrides before save method of base model"""
        if self.status not in PurchaseOrder.VALID_STATUSES:
            raise ValueError("Invalid status option passed for updating")

        if self.is_new:
            return

        old_instance = PurchaseOrder.objects.get(pk=self.pk)
        self.is_status_changed = self.status != old_instance
        self.is_acknowledging_now = (
            self.acknowledgment_date and not old_instance.acknowledgment_date
        )

    @property
    def is_completed(self):
        """A property which tells if the current PO is completed or not"""
        return self.status == PurchaseOrder.STATUS_COMPLETED

    @classmethod
    def calculate_on_time_deliveries_for_vendor(
        cls, completed_deliveries_for_current_vendor=[]
    ):
        """Calculates all on time deliveries for a vendor"""
        total_completed_deliveries = len(completed_deliveries_for_current_vendor)
        # If there are no total completed orders
        if not total_completed_deliveries:
            return 0

        on_time_deliveries = [
            delivery
            for delivery in completed_deliveries_for_current_vendor
            if (
                delivery.get("delivery_date") is not None
                and delivery.get("expected_delivery_date") is not None
                and delivery.get("delivery_date")
                <= delivery.get("expected_delivery_date")
            )
        ]

        # If there are no on time deliveries
        if not on_time_deliveries:
            return 0

        return math.round(
            float(len(on_time_deliveries)) / float(total_completed_deliveries), 2
        )

    @classmethod
    def calculate_quality_rating_avg(cls, completed_deliveries_for_current_vendor=[]):
        """Calculates average of quality ratings of completed orders for a vendor"""
        if not completed_deliveries_for_current_vendor:
            return Exception("Invalid vendor id!")

        all_ratings = [
            delivery.get("quality_rating")
            for delivery in completed_deliveries_for_current_vendor
            if delivery.get("quality_rating") is not None
        ]
        return (
            math.round(float(sum(all_ratings)) / len(all_ratings), 2)
            if all_ratings
            else None
        )

    @classmethod
    def acknowledge(cls, instance_id, payload, *args, **kwargs):
        """A method used for acknowledgement of a purchase order."""
        if not payload.get("purchase_order_id"):
            raise ValueError("Invalid payload!")

        purchase_order = cls.objects.filter(pk=instance_id)
        if not purchase_order.exists():
            raise ValueError("Purchase order does not exist")

        purchase_order = purchase_order.first()
        if purchase_order.acknowledgment_date:
            raise ValueError("Purchase order already acknowledged")

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save(update_filds=["acknowledgment_date"])
        return True
