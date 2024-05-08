from django.db import models
from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


from django.db import models

# Create your models here.
from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(null=False, default=0.0)
    average_response_time = models.FloatField(null=False, default=0.0)
    fullfillment_rate = models.FloatField(null=False, default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Vendor"


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor} - {self.date}"


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        u = update_on_time_delivery_rate(instance.vendor)
        print("===u", u)
        update_quality_rating_avg(instance.vendor)
    if instance.acknowledgment_date:
        update_average_response_time(instance.vendor)
    update_fulfillment_rate(instance.vendor)


def update_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivery_count = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    total_completed_pos = completed_pos.count()

    if total_completed_pos > 0:
        on_time_delivery_rate = on_time_delivery_count / total_completed_pos * 100
        print("===ontimedel", on_time_delivery_rate)
        HistoricalPerformance.objects.create(
            vendor=vendor,
            on_time_delivery_rate=on_time_delivery_rate
        )


def update_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']
    print("==qualrat", quality_rating_avg)
    if quality_rating_avg is not None:
        HistoricalPerformance.objects.create(
            vendor=vendor,
            quality_rating_avg=quality_rating_avg
        )


def update_average_response_time(vendor):
    completed_pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_acknowledgment]
    print("==restime", response_times)
    if response_times:
        average_response_time = sum(response_times) / len(response_times)
        print("===average_res_time", average_response_time)
        HistoricalPerformance.objects.create(
            vendor=vendor,
            average_response_time=average_response_time
        )


def update_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successful_fulfillments = total_pos.filter(status='completed', quality_rating__isnull=True).count()

    if total_pos.count() > 0:
        fulfillment_rate = successful_fulfillments / total_pos.count() * 100
        HistoricalPerformance.objects.create(
            vendor=vendor,
            fulfillment_rate=fulfillment_rate
        )


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    # Check if the signal has already been processed for this instance
    if not hasattr(instance, '_signal_processed'):
        if instance.status == 'completed':
            u = update_on_time_delivery_rate(instance.vendor)
            print("===u", u)
            update_quality_rating_avg(instance.vendor)
        if instance.acknowledgment_date:
            update_average_response_time(instance.vendor)
        update_fulfillment_rate(instance.vendor)

        # Mark the instance to indicate that the signal has been processed
        instance._signal_processed = True


