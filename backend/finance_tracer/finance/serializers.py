from rest_framework import serializers
from .models import Wallet, Category, Transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'category_type', 'is_global']
        read_only_fields = ['user']


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # Просто объявляем поле, DRF автоматически возьмет его из аннотации во View
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'name', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    # Сериализатор просто проверяет, существуют ли вообще такие ID в базе данных
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'category', 'description', 'created_at', 'wallet']

class TransferSerializer(serializers.Serializer):
    from_wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())
    to_wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    def validate(self, data):
        # Проверяем, что кошельки не совпадают
        if data['from_wallet'] == data['to_wallet']:
            raise serializers.ValidationError("Нельзя перевести деньги на тот же самый кошелек.")
        return data