from django.views.generic import ListView, DetailView
from django.db.models import Q
from functools import reduce
import operator

from .models import Item, ItemState, Category


class ItemListView(ListView):
    model = Item
    template_name = "items/item_list.html"
    context_object_name = "items"
    paginate_by = 4

    def get_queryset(self):
        queryset = Item.objects.select_related("category", "user").prefetch_related("photos").order_by("-created_at")

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

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["ItemState"] = ItemState
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "items/item_detail.html"
    context_object_name = "item"
