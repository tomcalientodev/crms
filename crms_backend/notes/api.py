from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers import serialize

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.models import User, Customer, OrganizationOwner
from accounts.serializers import UserSerializer, CustomerSerializer

from .forms import NoteForm, JobCreationForm
from .serializers import NoteSerializer, JobSerializer
from .models import Note, Job
from accounts.models import Employee 



###################
######Get Feeds#####
    
@api_view(['GET'])
def get_notes(request, customerId):
   customer = Customer.objects.get(id=customerId)
   notes = Note.objects.filter(related_customer=customer)

   jobs = Job.objects.filter(related_customer=customer)
   
   notes_serializer = NoteSerializer(notes, many=True)
   customer_serializer = CustomerSerializer(customer)
   jobs_serializer = JobSerializer(jobs, many=True)
   
   return JsonResponse({
        'notes': notes_serializer.data,
         'customer': customer_serializer.data,
         'jobs': jobs_serializer.data},
           safe=False)


@api_view(['GET'])
def get_job_leads(request):
    organization_id = set()

    #Get Organization id.
    if hasattr(request.user, 'organizationowner'):
        org_id = OrganizationOwner.objects.filter(user=request.user).values_list('organization_id', flat=True)
        organization_id.update(org_id)
    else:
      pass

    if hasattr(request.user, 'employee'):
       org_id = Employee.objects.filter(user=request.user).values_list('organization_id', flat=True)
       organization_id.update(org_id)
    
    # Fetch employees and organization owners for the specified organization
    employees = Employee.objects.filter(organization_id__in=organization_id).select_related('user')
    organization_owners = OrganizationOwner.objects.filter(organization_id__in=organization_id).select_related('user')
    
    # Serialize user details
    employee_data = [{'id': emp.user.id, 'first_name': emp.user.first_name, 'last_name': emp.user.last_name} for emp in employees]
    owner_data = [{'id': owner.user.id, 'first_name': owner.user.first_name, 'last_name': owner.user.last_name} for owner in organization_owners]
    
    leads = {
        'employees': employee_data,
        'organization_owners': owner_data
    }
    return JsonResponse({'leads': leads}, safe=False)


@api_view(['GET'])
def get_job_notes(request, customerId, jobId):

    try:
        customer = Customer.objects.get(id=customerId)
        job = Job.objects.get(id=jobId)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Customer or Job not found'}, status=404)
    
    notes = Note.objects.filter(related_customer=customer, related_job=job)

    notes_serializer = NoteSerializer(notes, many=True)
    customer_serializer = CustomerSerializer(customer)
    job_serializer = JobSerializer(job)
    

    return JsonResponse({
        'notes': notes_serializer.data,
         'customer': customer_serializer.data,
         'job': job_serializer.data,},
           safe=False)


@api_view(['GET'])
def get_job_status(request):
    '''Retrieve job status options from the model choices'''
    job_status_options = [status[0] for status in Job.JOB_STATUS]
    # Return the status options as JsonResponse
    return JsonResponse({'status': job_status_options})



################
#####Job CRUD###

@api_view(['POST'])
def job_creation(request, customerId):
    form = JobCreationForm(request.data)
    if form.is_valid():
        job = form.save(commit=False)
        customer = Customer.objects.get(id=customerId)
        job.related_customer_id = customer.id
        job.related_organization_id = customer.organization.id
        due_date =request.data.get('due_date')
        job.due_date = due_date
        job.save()
        serializer = JobSerializer(job)
        return JsonResponse({'message': 'success', 'job': serializer.data})
    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    

@api_view(['POST'])
def job_note_creation(request, customerId, jobId):
    form = NoteForm(request.data)
    if form.is_valid():
        note = form.save(commit=False)
        customer = Customer.objects.get(id=customerId)
        job = Job.objects.get(id=jobId)
        note.related_job_id = job.id
        note.related_customer_id = customer.id
        note.created_by = request.user
        note.save()
        serializer = NoteSerializer(note)
        return JsonResponse({'message': 'success', 'notes': serializer.data})
    else:
        # Handle invalid form data here
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    

@api_view(['GET'])
def get_jobs(request, customerId):
   customer = Customer.objects.get(id=customerId)
   jobs = Job.objects.filter(related_customer=customer)
   
   jobs_serializer = JobSerializer(jobs, many=True)
   customer_serializer = CustomerSerializer(customer)
   
   return JsonResponse({
        'jobs': jobs_serializer.data,
        'customer': customer_serializer.data,
         },
           safe=False)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()  # Base queryset of all jobs
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
            job_id = kwargs.get('pk')
            job = get_object_or_404(Job, id=job_id)

            lead_id = request.data.get('lead')
            lead_two_id = request.data.get('lead_two')
            if lead_id:
                job.lead = get_object_or_404(User, id=lead_id)
            if lead_two_id:
                job.lead_two = get_object_or_404(User, id=lead_two_id)

            serializer = self.get_serializer(job, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return JsonResponse({'message': 'success', 'job': serializer.data})
    





# @api_view(['POST'])
# def update_job(request, customerId, jobId):
#     #Get the job objects.
#     try:
#         job = Job.objects.get(id=jobId, related_customer=customerId)

#         lead_id = request.data.get('lead')
#         if lead_id:
#             lead_user =User.objects.get(id=lead_id)
#             job.lead = lead_user

#         job.name = request.data.get('name', job.name)
#         job.status = request.data.get('status', job.status)
#         job.save()

#     except Job.DoesNotExist:
#         return JsonResponse({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

#     except ValidationError as e: #I added this since django won't catch it due to blank=True.
#         return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e: 
#         return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     serializer = JobSerializer(job) #return the newly update fields.
#     return JsonResponse({'message': 'success', 'job': serializer.data})



############################
###### Misc Notes CRUD ######

@api_view(['POST'])
def misc_note_create(request, customerId):
    form = NoteForm(request.data)
    if form.is_valid():
        note = form.save(commit=False)
        customer = Customer.objects.get(id=customerId)
        note.related_customer_id = customer.id
        note.created_by = request.user
        note.save()
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.data, safe=False)
    else:
        # Handle invalid form data here
        return JsonResponse({'error': 'Invalid form data'}, status=400)

class NoteViewSet(viewsets.ModelViewSet):
    '''Deletes and Updates Misc Notes. Separate functon for Job Notes and Creating Notes.'''
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) #Retrieves the partial argument from kwargs, if it exists. If not, it defaults to False. This flag indicates whether the update is partial (PATCH) or full (PUT).
        instance = self.get_object() #Retrieves the instance of the Note model that is being updated, based on the URL parameters.
        data = request.data.copy() #Creates a copy of the request data to avoid modifying the original request data.
        data['updated_by_id'] = request.user.pk
        
        serializer = self.get_serializer(instance, data=data, partial=partial) #Creates a serializer instance with the existing Note instance and the updated data. Passes the partial flag to handle partial updates.
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer) #This method is provided by the ModelViewSet.

        if getattr(instance, '_prefetched_objects_cache', None): #Clearing this cache can be necessary in some cases to ensure that the data is accurate and up-to-date after an update. You might use optimized queries selct_related or prefetch_related later and want to keep this.
            # If 'prefetched_objects_cache' exists, it needs to be invalidated to prevent incorrect data from being returned.
            instance._prefetched_objects_cache = {} 

        return JsonResponse(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     note = self.get_object()
    #     note.delete()
    #     return JsonResponse(status=status.HTTP_204_NO_CONTENT)