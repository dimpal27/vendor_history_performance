from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializer import  PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.contrib.auth.models import User

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St',
            'vendor_code': 'TEST123'
        }

    def test_create_vendor(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('vendor-list-create')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

    # Add more test cases for other CRUD operations on vendors

class HistoricalPerformanceTestCase(TestCase):
    def setUp(self):
        self.vendor, _ = Vendor.objects.get_or_create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        HistoricalPerformance.objects.create(vendor=self.vendor, on_time_delivery_rate=100.0)

    def test_historical_performance_creation(self):
        historical_performances = HistoricalPerformance.objects.filter(vendor=self.vendor)
        self.assertEqual(historical_performances.count(), 1)
        historical_performance = historical_performances.first()
        self.assertEqual(historical_performance.on_time_delivery_rate, 100.0)
        self.assertIsNone(historical_performance.quality_rating_avg)
        # Add assertions for other performance metrics

    # Add more test cases for other functionality as needed

class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        self.purchase_order_data = {
            'po_number': 'PO123',
            'vendor': self.vendor.id,
            'order_date': '2024-04-30T10:00:00Z',
            'delivery_date': '2024-05-05T10:00:00Z',
            'items': [{'name': 'Item 1', 'quantity': 10}],
            'quantity': 10,
            'status': 'pending',
            'issue_date': '2024-04-30T10:00:00Z',
            'acknowledgment_date': None
        }

    def test_create_purchase_order(self):
        url = reverse('purchase-order-list-create')  # Ensure correct URL pattern name
        response = self.client.post(url, self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO123')

    # Add more test cases for other CRUD operations on purchase orders
