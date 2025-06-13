from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import (ItemCreateView, ItemDeleteView, ItemListView,
                       ItemRetrieveView, ItemUpdateView)

schema_view = get_schema_view(
    openapi.Info(
        title="Darunky API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="swagger_docs"),
    path("auth/", include("djoser.urls.jwt")),
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/<int:pk>/", ItemRetrieveView.as_view(), name="item-detail"),
    path("items/<int:pk>/update/", ItemUpdateView.as_view(), name="item-update"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
]
