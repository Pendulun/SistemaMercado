from django.db import models
from django.urls import reverse
from products.models import Product

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)

    def get_absolute_url(self):
        return reverse('suppliers:update', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name+":"+self.cnpj
    
    def __eq__(self, obj):
        if isinstance(obj, Supplier):
            conditions = [obj.name == self.name,
                            obj.telephone == self.telephone,
                            obj.cnpj == self.cnpj,
                            obj.address == self.address
                        ]
            return all(conditions)
        else:
            return False
    
    def __hash__(self):
        return super().__hash__()