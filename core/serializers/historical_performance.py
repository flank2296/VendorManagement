from rest_framework import serializers

from core.models.historical_performance import HistoricalPerformance


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"
