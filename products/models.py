from django.db import models
from django.contrib.auth.models import User


class products(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField()
    quantity = models.IntegerField(default=0,null=True)
    quantity_left = models.IntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return self.name