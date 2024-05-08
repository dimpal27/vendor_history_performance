from django.contrib import admin
from django.urls import path, include

from .views import VendorListCreateView, VendorRetrieveUpdateDeleteView, PurchaseOrderListCreateView, \
    PurchaseOrderRetrieveUpdateDeleteView, HistoricalPerformanceRetrieveView, PurchaseOrderAcknowledgmentAPIView

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(),
         name='purchase-order-retrieve-update-delete'),
    path('vendors/<int:vendor>/performance/', HistoricalPerformanceRetrieveView.as_view(),
         name='historical-performance-retrieve'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', PurchaseOrderAcknowledgmentAPIView.as_view(), name='acknowledge-purchase-order'),

]
