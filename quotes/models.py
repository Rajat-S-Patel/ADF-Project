from django.db import models
from Auth.models import CustomUser

class Stock(models.Model):
    ticker=models.CharField(max_length=10,primary_key=True)
    user=models.ManyToManyField(CustomUser)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker
