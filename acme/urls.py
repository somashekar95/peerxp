
from django.contrib import admin
from django.urls import path
from . import views
from .views import ManageTicketsView

urlpatterns = [
    path('',views.home2, name='home2'),
    path('login/', views.login_view, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('createuser/',views.create_user,name='createuser'),
    path('',views.home, name='home'),
    path('updatedept/<int:pk>',views.update_department,name='updatedept'),
    path('createdept/',views.create_department,name='createdept'),
    path('deletedept/<int:pk>',views.delete_department,name='deletedept'),
    # path('', views.home1, name='home1'),
    path('ticket/',views.create_ticket,name='ticket'),
    path('manage_tickets/', ManageTicketsView.as_view(), name='manage_tickets')
    # path('deleteticket/',views.delete_ticket,name='deleteticket'),
    
]

