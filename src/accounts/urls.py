from django.urls import path
from .views import (
    IndexView,
    UserLoginView,
    UserLogoutView,
    UserRegistration,
    UserActivationView,
    send_test_email,
)

app_name = "accounts"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegistration.as_view(), name="register"),
    path("activate/<uid>/<token>/", UserActivationView.as_view(), name="activate"),
    path("send-test-email/", send_test_email, name="send_test_email"),
]
