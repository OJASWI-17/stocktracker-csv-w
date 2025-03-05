from django.db import models
from django.contrib.auth.models import User

class StockDetail(models.Model):
    stock = models.CharField(max_length=50,unique=True)
    user = models.ManyToManyField(User)
    

    