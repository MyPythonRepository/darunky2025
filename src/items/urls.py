from django.urls import path
from .views import ItemListView, ItemDetailView

app_name = "items"

urlpatterns = [
    path('', ItemListView.as_view(), name="item_list"),
    path('<int:pk>/', ItemDetailView.as_view(), name="item_detail"),
]
