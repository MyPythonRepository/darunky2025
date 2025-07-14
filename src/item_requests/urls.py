from django.urls import path
from .views import RequestCreateView

app_name = "item_requests"

urlpatterns = [
    path("create/<int:item_id>/", RequestCreateView.as_view(), name="create"),
]
