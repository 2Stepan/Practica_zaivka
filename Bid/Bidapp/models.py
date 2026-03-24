from django.db import models

# Create your models here.
from django.db import models


class Request(models.Model):

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("done", "Завершена"),
        ("canceled", "Отменена"),
    ]

    client_name = models.CharField(
        max_length=255,
        verbose_name="Имя клиента"
    )

    contacts = models.CharField(
        max_length=255,
        verbose_name="Контакты"
    )

    service = models.CharField(
        max_length=255,
        verbose_name="Услуга"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заявка {self.id} - {self.client_name}"