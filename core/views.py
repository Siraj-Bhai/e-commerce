from rest_framework import viewsets, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Product, Order
from .serializers import (
    UserSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderCreateSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


# Pagination
class ProductPagination(PageNumberPagination):
    page_size = 5


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'price']

    def perform_create(self, serializer):
        if not self.request.user.is_seller:
            raise PermissionDenied("Only sellers can add products.")
        serializer.save(seller=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_buyer:
            return Order.objects.filter(buyer=user)
        elif user.is_seller:
            return Order.objects.filter(items__product__seller=user).distinct()
        return Order.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_buyer:
            raise PermissionDenied("Only buyers can place orders.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(buyer=request.user)

        read_serializer = OrderSerializer(order, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)