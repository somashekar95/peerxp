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

def assign_department(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        pk = request.POST.get('department')
        department = Department.objects.get(id=pk)
        user.department = department
        user.save()
        return redirect("dashboard")

    departments = Department.objects.all()

    return render(request, "acme/assign_department.html", {"user": user, "departments": departments})



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
    return redirect("home")





def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.email = request.user.email
            ticket.phone_number = request.user.phone_number
            ticket.save()

            # Post the new ticket to ZenDesk using their Create Ticket API
            response = requests.post(
                'https://your-zendesk-domain.zendesk.com/api/v2/tickets.json',
                headers={'Authorization': f'Bearer {your_zendesk_api_token}'},
                json={
                    'ticket': {
                        'subject': ticket.subject,
                        'comment': {
                            'body': ticket.body
                        },
                        'priority': ticket.priority,
                        'requester': {
                            'email': ticket.email,
                            'phone': ticket.phone_number
                        }
                    }
                }
            )

            if response.status_code == 201:
                messages.success(request, 'Your ticket has been created successfully!')
                return redirect('ticket_confirmation')
            else:
                messages.error(request, 'Something went wrong, please try again.')
    else:
        form = TicketForm()

    return render(request, 'acme/create_ticket.html', {'form': form})

@login_required
def ticket_confirmation(request):
    return render(request, 'acme/ticket_confirmation.html')


@login_required
def manage_tickets(request):
    if request.user.is_admin:
        # Fetch all tickets in the organization
        response = requests.get(
            'https://your-zendesk-domain.zendesk.com/api/v2/tickets.json',
            headers={'Authorization': f'Bearer {your_zendesk_api_token}'}
        )
    else:
        # Fetch all tickets created by the user
        response = requests.get(
            f'https://your-zendesk-domain.zendesk.com/api/v2/tickets/search.json?query=requester:{request.user.email}',
            headers={'Authorization': f'Bearer {your_zendesk_api_token}'}
        )

    tickets = response.json()['tickets']

    return render(request, 'acme/manage_tickets.html', {'tickets': tickets})

@login_required
def delete_ticket(request, id):
    # Check if the user is an admin
    if not request.user.is_admin:
        return redirect('tickets:manage_tickets')

    # Delete the ticket using the ZenDesk Delete Ticket API
    response = requests.delete(
        f'https://your-zendesk-domain.zendesk.com/api/v2/tickets/{id}.json',
        headers={'Authorization': f'Bearer {your_zendesk_api_token}'}
    )

    if response.status_code == 200:
        # If the ticket was deleted successfully, redirect the user back to the manage tickets page
        messages.success(request, 'Ticket deleted successfully.')
        return redirect('tickets:manage_tickets')
    else:
        # If the ticket could not be deleted, show an error message
        messages.error(request, 'Failed to delete ticket.')
        return redirect('tickets:manage_tickets')

