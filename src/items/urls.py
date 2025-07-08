from django.urls import path

from . import views
from .views import ItemListView, ItemDetailView, ItemCreateView

app_name = "items"

urlpatterns = [
    path("add/", ItemCreateView.as_view(), name="item_add"),
    path("", ItemListView.as_view(), name="item_list"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("<int:pk>/edit/", views.ItemUpdateView.as_view(), name="item_edit"),
    path("<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),
]
