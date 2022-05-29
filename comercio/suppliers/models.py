from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    #product list

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