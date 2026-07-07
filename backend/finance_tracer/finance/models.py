from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Доход'),
        ('EXPENSE', 'Расход'),
    ]

    # null=True и blank=True обязательны, чтобы логика is_global работала в базе
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=20)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Флаг для превращения категории в общедоступную администратором
    is_global = models.BooleanField(default=False)

    def __str__(self):
        status = 'Глобальная' if self.is_global else 'Личная'
        return f"{self.name} ({status})"

    # Автоматически очищаем юзера, если админ делает категорию глобальной
    def save(self, *args, **kwargs):
        if self.is_global:
            self.user = None
        super().save(*args, **kwargs)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return f"{self.amount} - {self.wallet.name}"