from django.db import models
from django.contrib.auth.models import User


class products(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.name