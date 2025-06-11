from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from config import settings
from .forms import UserRegistrationForm
from .services.emails import send_registration_email
from .utils.token_generator import TokenGenerator


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["some_key"] = {"name": "name"}
        return context


class UserLoginView(LoginView):
    pass


class UserLogoutView(LogoutView):
    pass


class UserRegistration(CreateView):
    template_name = "registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object: get_user_model() = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        send_registration_email(user_instance=self.object, request=self.request)

        return super().form_valid(form)


class UserActivationView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, uid, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uid))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            return HttpResponse("Wrong data!")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user)

            return super().get(request, *args, **kwargs)

        return HttpResponse("Wrong data!")


@login_required(login_url=reverse_lazy("login"))
def send_test_email(request: HttpRequest) -> HttpResponse:
    send_mail(
        subject="Darunky2025",
        message="Darunky2025",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
    )
    return HttpResponse("Done")
