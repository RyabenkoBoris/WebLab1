from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

def validate_birth_date(value):
    if value > timezone.now().date():
        raise ValidationError("Дата народження не може бути у майбутньому.")

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        default="other"
    )
    birth_date = models.DateField(null=True, blank=True, validators=[validate_birth_date])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username