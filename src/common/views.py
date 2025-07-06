from django.http import JsonResponse
from common.tasks import (
    generate_test_users,
    generate_test_categories,
    generate_test_items
)


def generate_users_view(request):
    generate_test_users.delay(5)
    return JsonResponse({"status": "Task started: generate users"})


def generate_categories_view(request):
    generate_test_categories.delay(5)
    return JsonResponse({"status": "Task started: generate categories"})


def generate_items_view(request):
    generate_test_items.delay(10)
    return JsonResponse({"status": "Task started: generate items"})
