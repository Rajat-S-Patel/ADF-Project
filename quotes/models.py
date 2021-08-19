from django.db import models
from django.db.models.fields import DateField, DateTimeField

class Stock(models.Model):
    ticker=models.CharField(max_length=10)
    user=models.CharField(max_length=20,default="guest")
   
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker
