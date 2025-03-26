from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """
    Custom User model that inherits from Django's AbstractUser.
    """
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Volunteer(models.Model):
    """
    Represents a volunteer in the system.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Custom User model reference
        on_delete=models.CASCADE,
        related_name="volunteers"  # Allows easy reverse lookup: user.volunteers.all()
    )
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"
