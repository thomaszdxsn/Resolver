from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Card(models.Model):
    seria_no = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Transaction(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)