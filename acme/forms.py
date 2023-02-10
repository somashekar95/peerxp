from django import forms
from .models import User
from .models import Department
from .models import Ticket

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(email=username)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid login")
            except User.DoesNotExist:
                try:
                    user = User.objects.get(phone_number=username)
                    if not user.check_password(password):
                        raise forms.ValidationError("Invalid login")
                except User.DoesNotExist:
                    raise forms.ValidationError("Invalid login")

        return self.cleaned_data



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password', 'department', 'role']

        


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "subject",
            "body",
            "priority",
            "contact_details",
            "email",
            "phone_number",
        ]
