from django.db import models

# Create your models here.

class contact(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    number=models.CharField(max_length=20)
    message=models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
    