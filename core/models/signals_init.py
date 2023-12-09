from django.db.models.signals import post_save

from .purchase_order import PurchaseOrder
from .signal_functions import purchase_order_post_save

# Signal for connecting PO post save with PO model
post_save.connect(purchase_order_post_save, sender=PurchaseOrder)
