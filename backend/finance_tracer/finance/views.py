from django.db import models
from django.db.models import Sum, Case, When, DecimalField, Value
from django.db.models.functions import Coalesce
from django.db import transaction as db_transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, Category, Transaction
from .serializers import WalletSerializer, CategorySerializer, TransactionSerializer, TransferSerializer


# --- КОШЕЛЬКИ (Просмотр списка личных кошельков и создание) ---
class WalletListCreateView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user).annotate(
            balance=Coalesce(
                Sum(
                    Case(
                        # Если доход — берем сумму как есть (плюс)
                        When(transaction__category__category_type='INCOME', then='transaction__amount'),
                        # Если расход — умножаем транзакцию на -1 (минус)
                        When(transaction__category__category_type='EXPENSE', then=-models.F('transaction__amount')),
                        output_field=DecimalField(),
                    )
                ),
                Value(0.00),
                output_field=DecimalField()
            )
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- КАТЕГОРИИ (Список и создание) ---
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user) | Category.objects.filter(is_global=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- КАТЕГОРИИ (Просмотр, изменение, удаление конкретной) ---
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


# --- ТРАНЗАКЦИИ (Просмотр истории и создание с автозаполнением типа) ---
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        chosen_wallet = serializer.validated_data['wallet']
        chosen_category = serializer.validated_data['category']

        # Короткая проверка безопасности: кошелек должен принадлежать текущему юзеру
        if chosen_wallet.user != self.request.user:
            return Response({"detail": "Неверный кошелек."}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем транзакцию, принудительно записывая тип из категории прямо в базу (для DBeaver)
        serializer.save(transaction_type=chosen_category.category_type)


# --- ПЕРЕВОД МЕЖДУ КОШЕЛКАМИ ---
class TransferAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_wallet_id = request.data.get('from_wallet')
        to_wallet_id = request.data.get('to_wallet')

        # Берем кошельки строго из wallet_set текущего авторизованного юзера
        try:
            from_wallet = request.user.wallet_set.get(id=from_wallet_id)
            to_wallet = request.user.wallet_set.get(id=to_wallet_id)
        except Wallet.DoesNotExist:
            return Response({"detail": "Кошелек не найден."}, status=status.HTTP_404_NOT_FOUND)

        amount = serializer.validated_data['amount']

        # Системные категории для переводов
        transfer_out_cat, _ = Category.objects.get_or_create(
            name="Перевод (Расход)", category_type="EXPENSE", is_global=True
        )
        transfer_in_cat, _ = Category.objects.get_or_create(
            name="Перевод (Доход)", category_type="INCOME", is_global=True
        )

        # Атомарная транзакция в БД
        with db_transaction.atomic():
            # 1. Списание (Расход)
            Transaction.objects.create(
                wallet=from_wallet,
                category=transfer_out_cat,
                transaction_type=transfer_out_cat.category_type,
                amount=amount,
                description=f"Перевод на кошелек {to_wallet.name}"
            )
            # 2. Зачисление (Доход)
            Transaction.objects.create(
                wallet=to_wallet,
                category=transfer_in_cat,
                transaction_type=transfer_in_cat.category_type,
                amount=amount,
                description=f"Перевод с кошелька {from_wallet.name}"
            )

        return Response({"detail": "Перевод успешно выполнен."}, status=status.HTTP_201_CREATED)