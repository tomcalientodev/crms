from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q
from accounts.models import Customer, OrganizationOwner, Employee
from notes.models import Job
from notes.serializers import JobSerializer
from accounts.serializers import  CustomerSerializer


#TODO: if no search result is returned, tell the front end to display a message or just do this on the frontend.
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    # Retrieve the organization ID of the logged-in user
    if hasattr(request.user, 'organizationowner'):
      user = request.user
      organization_owner = OrganizationOwner.objects.get(user=user)
      organization_id = organization_owner.organization.id
    else:
      pass

    # Retrieve the organization ID of the logged-in user.
    if hasattr(request.user, 'employee'):
      user = request.user
      employee = Employee.objects.get(user=user)
      organization_id = employee.organization.id
    else:
      pass

    # Perform the search query with organization filter
    customers = Customer.objects.filter(
        Q(user__last_name__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__phone_number__icontains=query) |
        Q(user__email__icontains=query), organization_id=organization_id, )
    
        # Perform the search query with organization filter for jobs
    jobs = Job.objects.filter(
        Q(name__icontains=query) |
        Q(status__icontains=query),
        related_organization_id=organization_id
    )

    serializer = CustomerSerializer(customers, many=True)
    job_serializer = JobSerializer(jobs, many=True)
    return JsonResponse({
      'customers': serializer.data,
      'jobs': job_serializer.data
      })



@api_view(['GET'])
def all_customers(request):
    
        # Retrieve the organization ID of the logged-in user
    if hasattr(request.user, 'organizationowner'):
      user = request.user
      organization_owner = OrganizationOwner.objects.get(user=user)
      organization_id = organization_owner.organization.id
    else:
      pass

    # Retrieve the organization ID of the logged-in user.
    if hasattr(request.user, 'employee'):
      user = request.user
      employee = Employee.objects.get(user=user)
      organization_id = employee.organization.id
    else:
      pass
    
    customers = Customer.objects.filter(organization_id=organization_id)
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse({
      'all_customers': serializer.data
      })
