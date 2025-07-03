from celery import shared_task

from items.models import Category, User
from utils.data_generator import (
    generate_users,
    generate_categories,
    generate_items,
)


@shared_task
def generate_test_users(n=5):
    generate_users(n)


@shared_task
def generate_test_categories(n=5):
    generate_categories(n)


@shared_task
def generate_test_items(n=10):
    users = list(User.objects.all())
    categories = list(Category.objects.all())
    if users and categories:
        generate_items(users, categories, n)
