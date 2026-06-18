from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, Customer, Employee, Organization, OrganizationOwner


class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "phone_number",  )
		error_messages = {
            'email': {
                'required': 'Please provide your email address.',
            },
            'first_name': {
                'required': 'Please provide your first name.',
            },
            'last_name': {
                'required': 'Please provide your last name.',
            },
            'phone_number': {
                'required': 'Please provide your phone number.',
            },
            'password1': {
                'required': 'Please provide a password.',
            },
            'password2': {
                'required': 'Please repeat your password.',
            },
        }

class OrganizationOwnerForm(forms.ModelForm):
	class Meta:
		model = OrganizationOwner
		fields = (  )

class EmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = (  )

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ( )
		

class OrganizationForm(forms.ModelForm):
	class Meta:
		model = Organization
		fields = ( "organization",  )

