from rest_framework.generics import (
    CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from items.models import Item
from api.serializers import ItemSerializer


class ItemCreateView(CreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemListView(ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemUpdateView(UpdateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemDeleteView(DestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemRetrieveView(RetrieveAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
