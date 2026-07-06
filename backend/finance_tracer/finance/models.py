from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Category(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Доход'),
        ('EXPENSE', 'Расход'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.amount} - {self.wallet.name}"