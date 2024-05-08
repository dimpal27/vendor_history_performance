from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import VenderSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, \
    PurchaseOrderAcknowledgmentSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance, update_average_response_time
# Create your views here.

from rest_framework import generics, status
from .models import Vendor


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VenderSerializer
    permission_classes = [IsAuthenticated]


class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VenderSerializer


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        return queryset


class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class HistoricalPerformanceRetrieveView(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    lookup_field = 'vendor'

    # def get_queryset(self):
    #     vendor_id = self.kwargs['vendor_id']  # Use kwargs to get the vendor_id from the URL
    #     print("===vendorid",vendor_id)
    #     queryset = HistoricalPerformance.objects.filter(vendor__id=vendor_id)
    #     print("==queryset", queryset)
    #     return queryset


class PurchaseOrderAcknowledgmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(pk=po_id)

        # Check if the purchase order has already been acknowledged
        if purchase_order.acknowledgment_date:
            return Response({"detail": "Purchase Order already acknowledged."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PurchaseOrderAcknowledgmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update acknowledgment date in the purchase order
        purchase_order.acknowledgment_date = serializer.validated_data['acknowledgment_date']
        purchase_order.save()

        # Trigger the recalculation of average_response_time
        update_average_response_time(purchase_order.vendor)

        return Response({"detail": "Purchase Order acknowledged successfully."}, status=status.HTTP_200_OK)