from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import OrganizationForm, OrganizationOwnerForm, UserForm, CustomerForm, EmployeeForm
from .models import User, Organization, OrganizationOwner, Customer, Employee

from rest_framework import status, viewsets

from .serializers import EmployeeSerializer, CustomerSerializer, updateCustomerSerializer
from.permissions import IsOrganizationOwner
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


@api_view(['GET']) #not including aut_classes because we want CORS to do this.
def user_info(request):
    '''Sends logged on user info to frontend as user.'''
    user_data = request.user
    # checks if the user_data object is not an instance of the AnonymousUser.
    if not isinstance(user_data, AnonymousUser):
        organization_name = None
        try:
            organization_owner = OrganizationOwner.objects.get(user=request.user)
            organization_name = organization_owner.organization.organization

        except OrganizationOwner.DoesNotExist:
            pass
        
        if not organization_name:
            try:
                employee = Employee.objects.get(user=user_data)
                organization_name = employee.organization.organization
            except Employee.DoesNotExist:
                logger.warning(f"User {user_data.email} is neither an Organization Owner nor an Employee.")
                return JsonResponse({'error': 'User does not have an associated organization.'}, status=404)
    else:
        # Handle the case where the user is not authenticated
        logger.warning(f"User {user_data.email} user is not authenicated.") 

    user = {
        'id': user_data.id,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'email': user_data.email,
        'organization_name': organization_name,
    }
    return JsonResponse(user)

from django.db import IntegrityError

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsOrganizationOwner]

    def get_queryset(self):
        # Get the logged-in user's organization
        user_id = self.request.user.id
        org_owner = OrganizationOwner.objects.get(user_id=user_id)
        organization = org_owner.organization_id
        return Employee.objects.filter(organization_id=organization)
    
    def create(self, request):
        '''Allows organization owners only to create employees.'''
        user_form = UserForm(request.data)
        employee_form = EmployeeForm(request.data)
        if (user_form.is_valid() and employee_form.is_valid()):
            print('made it to valid checks')
            # Save new user and add user id to employee.
            user = user_form.save(commit=False)
            employee = employee_form.save(commit=False)
            employee.user = user
            # Get OrganizationOwner, save to employee.
            user_id = request.user.id
            org_owner = OrganizationOwner.objects.get(user_id=user_id)
            employee.organization = org_owner.organization
            # Save employee form.
            user_form.save()
            employee_form.save()
            return JsonResponse({'message': 'success'}, status=status.HTTP_201_CREATED)
        else:
            message = user_form.errors.as_json()
            return JsonResponse({'message': message})
        
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_data = serializer.validated_data

        # Update only if field is present and different
        for field, value in updated_data.items():
            if field == 'user':
                user_data = updated_data.get('user', {})
                if 'email' in user_data:
                    # Only update email if the new email is not empty or different from the current value
                    new_email = user_data['email']
                    if new_email and new_email != instance.user.email:
                        instance.user.email = new_email

                # Update other fields of the user
                for user_field, user_value in user_data.items():
                    if user_field != 'email' and getattr(instance.user, user_field) != user_value:
                        setattr(instance.user, user_field, user_value)
            elif getattr(instance, field) != value:
                setattr(instance, field, value)

        # Save the instance and user object
        instance.user.save()
        instance.save()
        return JsonResponse(serializer.data)
        


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerSerializer
        if self.action in ['update', 'partial_update']:
            return updateCustomerSerializer
        return super().get_serializer_class()

    def create(self, request):
        if request.method == "POST":
            message = 'success'
            user_form = UserForm(request.data)
            customer_form = CustomerForm(request.data)
            if (user_form.is_valid() and customer_form.is_valid()):
                #Save new user and add user id to customer.
                user = user_form.save(commit=False)
                customer_form = customer_form.save(commit=False)
                customer_form.user = user
                #Get Organization, save to customer.
                user = request.user.id
                if hasattr(request.user, 'organizationowner'):
                    org_owner = OrganizationOwner.objects.get(user=user)
                    customer_form.organization = org_owner.organization
                elif hasattr(request.user, 'employee'):
                    emp = Employee.objects.get(user=user)
                    customer_form.organization = emp.organization
                #Save customer form.
                user_form.save()
                customer_form.save()
            else:
                message = user_form.errors.as_json()
                return JsonResponse({'message': message})
        return JsonResponse({'message': message})
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        user_data = serializer.validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            # user.email = user_data.get('email', user.email)
            user.phone_number = user_data.get('phone_number', user.phone_number)
            if 'email' in user_data:
                user.email = user_data['email']
            user.save()

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(serializer.data)

    
    
@api_view(['POST'])
@authentication_classes([])  # Consider authentication for security
@permission_classes([])
@transaction.atomic  # Wrap logic in case a form fails, neither are saved.
def create_organization_and_owner(request):
    if request.method == "POST":
        message = 'success'
        detailed_errors = []

        # Create organization.
        organization_form = OrganizationForm(request.data)
        # Check organization form validity within the transaction
        if not organization_form.is_valid():
            message = organization_form.errors.as_json()
            return JsonResponse({'message': message})

        # Create user.
        user_form = UserForm(request.data)
        # Check user form validity within the transaction
        if not user_form.is_valid():
            message = user_form.errors.as_json()
            return JsonResponse({'message': message})
        
        # Validate password
        password = user_form.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            detailed_errors.extend(list(e.messages))
            message = 'Password validation failed.'
            return JsonResponse({'message': message, 'errors': detailed_errors})

        # Save organization and user within the transaction
        organization = organization_form.save()
        user = user_form.save()

        # Create the OrganizationOwner object
        organization_owner = OrganizationOwner.objects.create(
            user=user,
            organization=organization
        )
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Invalid request method.'})






 
# Can delete, turned into a ViewSet
# @api_view(['POST'])
# def create_customer(request):
#     '''Allows Employees and Organization Owners to create customers.'''
#     if request.method == "POST":
#         message = 'success'
#         user_form = UserForm(request.data)
#         customer_form = CustomerForm(request.data)
#         if (user_form.is_valid() and customer_form.is_valid()):
#             #Save new user and add user id to customer.
#             user = user_form.save(commit=False)
#             customer_form = customer_form.save(commit=False)
#             customer_form.user = user
#             #Get Organization, save to customer.
#             user = request.user.id
#             if hasattr(request.user, 'organizationowner'):
#                 org_owner = OrganizationOwner.objects.get(user=user)
#                 customer_form.organization = org_owner.organization
#             elif hasattr(request.user, 'employee'):
#                 emp = Employee.objects.get(user=user)
#                 customer_form.organization = emp.organization
#             #Save customer form.
#             user_form.save()
#             customer_form.save()
#         else:
#             message = user_form.errors.as_json()
#             return JsonResponse({'message': message})
#     return JsonResponse({'message': message})