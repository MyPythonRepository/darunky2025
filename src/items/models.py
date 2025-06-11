from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel

User = get_user_model()


class ItemState(models.IntegerChoices):
    NEW = 1, "New"
    USED = 2, "Used"


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Item(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    state = models.PositiveSmallIntegerField(
        choices=ItemState.choices,
        default=ItemState.NEW
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name="items"
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="given_items"
    )

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class ItemPhoto(BaseModel):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    image_url = models.ImageField(upload_to="items/photos")

    def __str__(self):
        return f"Photo for {self.item.name} (ID: {self.item.id})"
