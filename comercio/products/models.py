from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    brand = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()

    def __str__(self):
        return self.name+":"+self.brand