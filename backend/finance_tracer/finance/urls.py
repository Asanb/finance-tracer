from django.urls import path
from .views import (
    WalletListCreateView,
    CategoryListCreateView,
    CategoryDetailView,
    TransactionListCreateView,
    TransferAPIView,
)

urlpatterns = [
    # Кошельки
    path('wallets/', WalletListCreateView.as_view(), name='wallets'),

    # Категории
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Транзакции
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
    #Перевод между кошелками
    path('transfer/', TransferAPIView.as_view(), name='transfer'),
]