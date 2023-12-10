from rest_framework import serializers

from core.models.purchase_order import PurchaseOrder


class PurchaseOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
