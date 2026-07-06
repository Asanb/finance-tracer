from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Category, Transaction

# Сериализатор для Кошельков
class WalletSerializer(serializers.ModelSerializer):
    # Выводим имя владельца текстом, а не просто ID цифрой
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'name', 'balance', 'currency']
        # Баланс защищаем от ручного изменения через API, он должен меняться только через транзакции
        read_only_fields = ['balance']


# Сериализатор для Категорий
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'type']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'category', 'created_at', 'wallet' ]
        read_only_fields = ['user']