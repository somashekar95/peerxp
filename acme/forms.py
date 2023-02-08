from django import forms
from .models import UserProfile,Department,Ticket
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Name', 'email', 'phone_number','department','role']
        widgets = {
            'password': forms.PasswordInput(),
        }


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = UserProfile
#         fields = ['Name', 'email', 'password1', 'password2']
#         def save(self, commit=True):
#             user = super().save(commit=False)
#             user.email = self.cleaned_data['email']
#             if commit:
#                 user.save()
#                 return user


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        
 

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'body', 'priority']

