
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('createuser/',views.create_user,name='createuser'),
    path('updatedept/',views.update_department,name='updatedept'),
    path('createdept/',views.create_department,name='createdept'),
    path('deletedept/',views.delete_department,name='deletedept'),
    path('ticket/',views.create_ticket,name='ticket'),
    path('manageticket/',views.manage_tickets,name='manageticket')
    
]

