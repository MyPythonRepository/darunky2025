from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from functools import reduce
import operator

from .models import Item, ItemState, Category, ItemPhoto
from .forms import ItemForm
from item_requests.models import Request


class ItemListView(ListView):
    model = Item
    template_name = "items/item_list.html"
    context_object_name = "items"
    paginate_by = 4

    def get_queryset(self):
        queryset = Item.objects.select_related("category", "user").prefetch_related("photos")

        query = self.request.GET.get("q")
        if query:
            keywords = query.split()
            q_objects = []
            for word in keywords:
                q_objects.append(
                    Q(name__icontains=word) |
                    Q(description__icontains=word) |
                    Q(category__name__icontains=word) |
                    Q(state__in=[state for state, label in ItemState.choices if word.lower() in label.lower()])
                )
            queryset = queryset.filter(reduce(operator.or_, q_objects))

        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        state = self.request.GET.get("state")
        if state:
            queryset = queryset.filter(state=state)

        user = self.request.user
        if user.is_authenticated:
            requested_items_ids = Request.objects.filter(requester=user).values_list("item_id", flat=True)
            queryset = queryset.filter(
                Q(user=user) | Q(is_requested=False) | Q(id__in=requested_items_ids)
            )
        else:
            queryset = queryset.filter(is_requested=False)

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["ItemState"] = ItemState
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "items/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        user = self.request.user

        context["is_owner"] = user == item.user
        context["has_requested"] = (
            item.item_requests.filter(requester=user).exists()
            if user.is_authenticated else False
        )
        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    template_name = "items/item_form.html"
    success_url = reverse_lazy("items:item_list")

    def form_valid(self, form):
        form.instance.user = self.request.user

        category_name = form.cleaned_data["category_name"].strip()
        category, _ = Category.objects.get_or_create(name__iexact=category_name, defaults={"name": category_name})
        form.instance.category = category

        self.object = form.save()

        photo_file = form.cleaned_data.get("photo")
        if photo_file:
            ItemPhoto.objects.create(item=self.object, image_url=photo_file)

        return redirect(self.success_url)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "items/item_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user

        category_name = form.cleaned_data["category_name"].strip()
        category, _ = Category.objects.get_or_create(name__iexact=category_name, defaults={"name": category_name})
        form.instance.category = category

        self.object = form.save()

        photo_file = form.cleaned_data.get("photo")
        if photo_file:
            self.object.photos.all().delete()
            ItemPhoto.objects.create(item=self.object, image_url=photo_file)

        return redirect("items:item_detail", pk=self.object.pk)

    def test_func(self):
        return self.request.user == self.get_object().user


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = "items/item_confirm_delete.html"
    success_url = reverse_lazy("items:item_list")

    def test_func(self):
        return self.request.user == self.get_object().user
