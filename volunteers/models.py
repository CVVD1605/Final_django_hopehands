from django.db import models


class Volunteer(models.Model):
    """
    Represents a volunteer application.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')  # ✅ New Field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        print("Debug: models.py loaded")
        return f"{self.username} - {self.first_name} {self.last_name}"
