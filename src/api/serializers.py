from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer

from items.models import Category, Item, ItemPhoto

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "is_staff"]


class ItemPhotoSerializer(ModelSerializer):
    class Meta:
        model = ItemPhoto
        fields = ["id", "image_url"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ItemSerializer(ModelSerializer):
    category = CharField(write_only=True)
    category_data = CategorySerializer(read_only=True, source="category")
    photos = ItemPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id", "name", "description", "state",
            "category", "category_data",
            "user", "photos",
        ]
        read_only_fields = ["user"]

    def _get_or_create_category(self, category_name):
        name = category_name.strip().title()
        category, _ = Category.objects.get_or_create(name=name)
        return category

    def create(self, validated_data):
        category_name = validated_data.pop("category")
        validated_data["category"] = self._get_or_create_category(category_name)
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "category" in validated_data:
            category_name = validated_data.pop("category")
            validated_data["category"] = self._get_or_create_category(category_name)
        return super().update(instance, validated_data)
