
from django.db import models
from django.contrib.auth.models import User
from django import forms

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
  

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('user', 'user'),
    )

    Name = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_by = models.ForeignKey(User, related_name='created_by_user', null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Ticket(models.Model):
    PRIORITY_CHOICES = (
        ('high', 'high'),
        ('medium', 'medium'),
        ('low', 'low'),
    )

    subject = models.CharField(max_length=255)
    body = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

