from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'


class PurchaseOrderAcknowledgmentSerializer(serializers.Serializer):
    acknowledgment_date = serializers.DateTimeField()

    def validate_acknowledgment_date(self, value):
        # You can add any validation logic here if needed
        return value

