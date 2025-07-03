from django.contrib.auth import get_user_model
from items.models import Category, Item, ItemState
from faker import Faker
import random

fake = Faker()
User = get_user_model()


def generate_users(n=5):
    users = []
    for _ in range(n):
        user = User.objects.create_user(
            email=fake.unique.email(),
            password="password12345678",
            name=fake.name(),
        )
        users.append(user)
    return users


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
