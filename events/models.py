from django.db import models
from django.contrib.auth.models import User
from products.models import products
# Create your models here.

class events(models.Model):
    client_name = models.CharField(max_length=500)
    event_location = models.CharField(max_length=500)
    shipment_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=500)
    google_event_id = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.client_name

class event_products(models.Model):
    quantity = models.CharField(max_length=500)
    event_products = models.ForeignKey(products, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(events, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.event.client_name
