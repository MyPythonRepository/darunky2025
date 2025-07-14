from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel
from faker import Faker
import random

fake = Faker()
User = get_user_model()


class ItemState(models.IntegerChoices):
    NEW = 1, "New"
    USED = 2, "Used"


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Item(BaseModel):
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    state = models.PositiveSmallIntegerField(choices=ItemState.choices, default=ItemState.NEW)

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, related_name="items")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="given_items")

    is_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class ItemPhoto(BaseModel):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, related_name="photos")
    image_url = models.ImageField(upload_to="items/photos")

    def __str__(self):
        return f"Photo for {self.item.name} (ID: {self.item.id})"


def generate_categories(n=5):
    categories = []
    for _ in range(n):
        cat = Category.objects.create(name=fake.unique.word())
        categories.append(cat)
    return categories


def generate_items(users, categories, n=10):
    items = []
    for _ in range(n):
        item = Item.objects.create(
            name=fake.word(),
            description=fake.text(),
            state=random.choice([ItemState.NEW, ItemState.USED]),
            user=random.choice(users),
            category=random.choice(categories),
        )
        items.append(item)
    return items
