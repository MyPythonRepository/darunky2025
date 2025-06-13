from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED)
from rest_framework.test import APIClient

from items.models import Category, Item

User = get_user_model()


class ItemApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.com", password="Pass*123")
        self.category = Category.objects.create(name="Books")
        self.item = Item.objects.create(
            name="Test Item", description="desc", state=1,
            category=self.category, user=self.user
        )
        self.urls = {
            "list": reverse("item-list"),
            "create": reverse("item-create"),
            "detail": reverse("item-detail", kwargs={"pk": self.item.pk}),
            "update": reverse("item-update", kwargs={"pk": self.item.pk}),
            "delete": reverse("item-delete", kwargs={"pk": self.item.pk}),
        }

    def test_auth_required_for_list(self):
        res = self.client.get(self.urls["list"])
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)

    def test_list_items_authenticated(self):
        self.client.force_authenticate(self.user)
        res = self.client.get(self.urls["list"])
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Test Item")

    def test_create_item(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(self.urls["create"], {
            "name": "New Item",
            "description": "desc",
            "state": 1,
            "category": self.category.name,
        })
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertTrue(Item.objects.filter(name="New Item", user=self.user).exists())

    def test_update_item_by_owner(self):
        self.client.force_authenticate(self.user)
        res = self.client.put(self.urls["update"], {
            "name": "Updated",
            "description": "Updated desc",
            "state": 2,
            "category": self.category.name,
        })
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated")

    def test_delete_item_by_owner(self):
        self.client.force_authenticate(self.user)
        res = self.client.delete(self.urls["delete"])
        self.assertEqual(res.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())
