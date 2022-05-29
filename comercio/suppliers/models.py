from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    #product list

    def __str__(self):
        return self.name+""+self.cnpj