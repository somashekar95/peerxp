
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import UserForm,DepartmentForm,TicketForm
from .models import Department,Ticket
import requests
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid login credentials. Please try again.'
            return render(request, 'acme/login.html', {'error': error})
    return render(request, 'acme/login.html')


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('UserProfile')
    else:
        form = UserForm()
    return render(request, 'acme/create_user.html', {'form': form})



def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.created_by = request.user
            department.save()
            return redirect('department_list')
        
    else:
        form = DepartmentForm()
    return render(request, 'acme/create_department.html', {'form': form})
# def department_list(request):
#     departments = Department.objects.all()
#     return render(request, 'acme/department_list.html', {'departments': departments})

def update_department(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'acme/update_department.html', {'form': form})

def delete_department(request, pk):
    department = Department.objects.get(pk=pk)
    if not department.user_set.exists():
        department.delete()
        return redirect('department_list')
    else:
        return render(request, 'acme/error.html', {'message': 'Department cannot be deleted as it is associated with a user'})
    


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            user = request.user  # get user information from the database
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            priority = form.cleaned_data['priority']
            contact_details = UserProfile.email + ' ' + UserProfile.phone_number  # concatenate user information
            email = UserProfile.email
            phone_number = UserProfile.phone_number
            ticket = Ticket(subject=subject, body=body, priority=priority, contact_details=contact_details, email=email, phone_number=phone_number)
            ticket.save()

            # Make a post request to the ZenDesk API to create a new ticket
            url = 'https://yoursubdomain.zendesk.com/api/v2/tickets.json'
            headers = {'Content-Type': 'application/json', 'Authorization': 'Basic your_base64_encoded_credentials'}
            data = {
                "ticket": {
                    "subject": subject,
                    "comment": {
                        "body": body
                    },
                    "priority": priority,
                    "requester": {
                        "name": contact_details,
                        "email": email,
                        "phone": phone_number
                    }
                }
            }
            response = requests.post(url, headers=headers, json=data)

            # Check the response status code and show a confirmation message to the user
            if response.status_code == 201:
                return render(request, 'acme/ticket_created.html', {'ticket': ticket})
    else:
        form = TicketForm()
    return render(request, 'acme/create_ticket.html', {'form': form})




def manage_tickets(request):
    user = request.user
    if user.is_superuser:  # if the user is an admin
        # Make a get request to the ZenDesk API to get a list of all tickets in the organization
        url = 'https://yoursubdomain.zendesk.com/api/v2/tickets.json'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic your_base64_encoded_credentials'}
        response = requests.get(url, headers=headers)
        tickets = response.json()['Ticket']
    else:
        # Make a get request to the ZenDesk API to get a list of all tickets created by the user
        url = 'https://yoursubdomain.zendesk.com/api/v2/search.json?query=requester:{}'.format(user.email)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic your_base64_encoded_credentials'}
        response = requests.get(url, headers=headers)
        tickets = response.json()['results']

    return render(request, 'acme/manage_tickets.html', {'tickets': tickets})

def delete_ticket(request, ticket_id):
    # Make a delete request to the ZenDesk API to delete a selected ticket
    url = 'https://yoursubdomain.zendesk.com/api/v2/tickets/{}.json'.format(ticket_id)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic your_base64_encoded_credentials'}
    response = requests.delete(url, headers=headers)

    # Check the response status code and redirect the user to the manage tickets page
    if response.status_code == 200:
        return redirect('manage_tickets')
