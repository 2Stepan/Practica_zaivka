from django.db import models

# Create your models here.
from django.db import models

class users(models.Model):
    ROLE_CHOICES = [
        ('designer', 'Дизайнер'),
        ('backend', 'Программист Backend'),
        ('frontend', 'Программист Frontend'),
        ('fullstack', 'Fullstack-разработчик'),
        ('manager', 'Менеджер'),
    ]

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='designer')

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
    client_email = models.EmailField(
        verbose_name="Email клиента"
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
    
    def update_task(self, new_service=None, new_description=None, new_status=None):
        if new_service is not None:
            self.service = new_service
        if new_description is not None:
            self.description = new_description
        if new_status is not None:
            self.status = new_status
        self.save()
        return self