from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib import messages
from .forms import DepartmentForm,UserForm,TicketForm
from .models import Department, User,Ticket
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.views.generic.base import TemplateView


def home2(request):
    return render(request, 'acme/home2.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data.get("user")
        request.session["user_id"] = user.id
        return redirect("home2")

    return render(request, "acme/login.html", {"form": form})




def dashboard(request):
    users = User.objects.all()
    return render(request, "acme/dashboard.html", {"users": users})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = UserForm()

    return render(request, "acme/create_user.html", {"form": form})



def home(request):
    departments = Department.objects.all()
    return render(request, "acme/home.html", {"departments": departments})


def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = DepartmentForm()

    return render(request, "acme/create_department.html", {"form": form})


def update_department(request, pk):
    department = Department.objects.get(id=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = DepartmentForm(instance=department)

    return render(request, "acme/update_department.html", {"form": form})

def delete_department(request, pk):
    department = Department.objects.get(id=pk)
    users = User.objects.filter(department=department)
    if users.count() > 0:
        messages.error(request, "Cannot delete department that is associated with a user.")
        return redirect("home")

    department.delete()
    form = DepartmentForm(instance=department)

    return render(request, "acme/delete_department.html", {"form": form})




import base64

def ticket_created(request):
    users = User.objects.all()
    return render(request, "acme/ticket_created.html", {"users": users})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            priority = form.cleaned_data['priority']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            # Your ZenDesk API credentials
            auth = base64.b64encode("{}:{}".format("username", "password").encode()).decode()
            headers = {
                "Authorization": "Basic {}".format(auth),
                "Content-Type": "application/json"
            }

            # The data to create a new ticket
            ticket_data = {
                "ticket": {
                    "subject": subject,
                    "comment": {
                        "body": body
                    },
                    "priority": priority,
                    "requester": {
                        "email": email,
                        "phone": phone_number
                    }
                }
            }

            # Post the ticket to ZenDesk API
            response = requests.post("https://{}.zendesk.com/api/v2/tickets.json".format("your_subdomain"), headers=headers, json=ticket_data)

            if response.status_code == 201:
                # Ticket created successfully, redirect to confirmation page
                return redirect("ticket_created")
            else:
                # Error creating the ticket, show error message
                return render(request, "acme/create_ticket.html", {"form": form, "error": "Error creating ticket"})
    else:
        form = TicketForm()

    return render(request, "acme/create_ticket.html", {"form": form})




class ManageTicketsView(TemplateView):
    template_name = 'acme/manage_tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_staff:
            # Fetch all tickets for Admins
            context['tickets'] = Ticket.objects.all()
        else:
            # Fetch all tickets created by the User
            context['tickets'] = Ticket.objects.filter(created_by=user)
        return context




