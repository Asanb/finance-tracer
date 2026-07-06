from rest_framework import generics
from .models import Wallet, Category
from .serializers import WalletSerializer, CategorySerializer


class WalletListCreateView(generics.ListCreateAPIView):
    # 1. Укажи, какой сериализатор использовать
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        user_cats = Category.objects.filter(user=self.request.user)
        global_cats = Category.objects.filter(user__isnull=True)
        return user_cats | global_cats
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)