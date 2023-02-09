from django.contrib import admin
from .models import Department,Ticket,User

# Register your models here.
admin.site.register(Department)
admin.site.register(Ticket)