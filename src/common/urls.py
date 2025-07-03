from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.generate_categories_view),
    path('users/', views.generate_users_view),
    path('items/', views.generate_items_view),
]
