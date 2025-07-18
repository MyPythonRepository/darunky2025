from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from items.models import Item
from .forms import RequestForm
from .models import Request


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = "item_requests/request_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.item = self.get_item()

        if Request.objects.filter(item=self.item, requester=request.user).exists():
            messages.error(request, "You have already sent a request for this item.")
            return redirect("items:item_detail", pk=self.item.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.item = self.item
        form.instance.giver = self.item.user
        form.instance.requester = self.request.user

        self.item.is_requested = True
        self.item.save(update_fields=["is_requested"])

        messages.success(self.request, "Your request has been sent.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.item
        context["is_owner"] = self.request.user == self.item.user
        return context

    def get_success_url(self):
        return reverse("items:item_detail", kwargs={"pk": self.item.id})

    def get_item(self):
        return get_object_or_404(Item, id=self.kwargs["item_id"])
