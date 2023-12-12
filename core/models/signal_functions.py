import math

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.historical_performance import HistoricalPerformance
from core.models.purchase_order import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(
    sender: models.Model, instance: PurchaseOrder, **kwargs: dict
):
    """Purchaes order pre save signals"""
    historical_fields_to_update = []
    completed_orders_for_vendor = PurchaseOrder.objects.filter(
        vendor_id=instance.vendor_id,
        status=PurchaseOrder.STATUS_COMPLETED,
    ).values(
        "delivery_date",
        "expected_delivery_date",
        "quality_rating",
        "issue_date",
        "acknowledgment_date",
    )

    vendors_perf = HistoricalPerformance.objects.get_or_create(
        vendor_id=instance.vendor_id
    )
    if instance.is_status_changed and instance.is_completed:
        vendors_perf.on_time_delivery_rate = (
            PurchaseOrder.calculate_on_time_deliveries_for_vendor(
                vendor_id=instance.vendor_id,
                completed_deliveries_for_current_vendor=completed_orders_for_vendor,
            )
        )
        historical_fields_to_update.append("on_time_delivery_rate")

        if instance.quality_rating:
            vendors_perf.quality_rating_avg = (
                PurchaseOrder.calculate_quality_rating_avg(
                    vendor_id=instance.vendor_id,
                    completed_deliveries_for_current_vendor=completed_orders_for_vendor,
                )
            )
            historical_fields_to_update.append("quality_rating_avg")

    if instance.is_status_changed:
        no_of_vendor_orders = PurchaseOrder.objects.filter(
            vendor_id=instance.vendor_id
        ).count()
        vendors_perf.fulfillment_rate = math.round(
            len(completed_orders_for_vendor) / no_of_vendor_orders, 2
        )
        historical_fields_to_update.append("fulfillment_rate")

    historical_fields_to_update and vendors_perf.save(
        update_fields=historical_fields_to_update
    )
