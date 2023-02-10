
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User as AuthUser


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    password = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=100)
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.email




class Ticket(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    priority = models.CharField(max_length=20)
    contact_details = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.subject

