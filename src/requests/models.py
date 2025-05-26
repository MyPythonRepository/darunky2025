from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel

User = get_user_model()


class Request(BaseModel):
    item = models.ForeignKey(
        to="items.Item",
        on_delete=models.CASCADE,
        related_name="requests",
        verbose_name="Item"
    )
    giver = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="given_requests",
        verbose_name="Giver"
    )
    requester = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="made_requests",
        verbose_name="Requester"
    )

    name = models.CharField(max_length=255, verbose_name="Name")
    phone = models.CharField(max_length=50, verbose_name="Phone")
    delivery_address = models.TextField(verbose_name="Delivery address")

    def get_short_name(self):
        return self.name

    def __str__(self):
        return f"Request #{self.id} for {self.item.name} by {self.requester.get_short_name()}"
