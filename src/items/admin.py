from django.contrib import admin
from items.models import Item, Category, ItemPhoto

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemPhoto)
