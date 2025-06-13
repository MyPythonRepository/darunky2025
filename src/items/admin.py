from django.contrib import admin

from items.models import Category, Item, ItemPhoto

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemPhoto)
