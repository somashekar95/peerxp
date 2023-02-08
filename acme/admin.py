from django.contrib import admin
from .models import Department,UserProfile,Ticket

# Register your models here.
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Ticket)