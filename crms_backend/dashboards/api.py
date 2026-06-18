
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from notes.serializers import JobSerializer
from .models import RecentlyViewedCustomer
from accounts.models import User, Customer
from notes.models import Job
from .models import RecentlyViewedCustomer
from accounts.serializers import UserSerializer, CustomerSerializer
from .serializers import RecentlyViewedCustomerSerializer




@api_view(['GET'])
def lead_jobs(request, workerId):

    jobs = Job.objects.filter(
        Q(lead=workerId) | Q(lead_two=workerId)
    )
    job_serializer = JobSerializer(jobs, many=True)
    return JsonResponse({
         'jobs': job_serializer.data,
    }, safe=False)


class RecentlyViewedCustomerViewSet(viewsets.ModelViewSet):
    queryset = RecentlyViewedCustomer.objects.all()
    serializer_class = RecentlyViewedCustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    MAX_RECENTLY_VIEWED = 7  # Define the limit here

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-viewed_at')

    def create(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk')
        user = request.user
        #Check if the RecentlyViewedCustomer already exists for this user and customer_id
        # Assuming customer_id is an integer, adjust the condition if it's different
        if RecentlyViewedCustomer.objects.filter(user=user.id, customer_id=customer_id).exists():
            return JsonResponse({'message': 'RecentlyViewedCustomer already exists'})
        else:
         # Create a new RecentlyViewedCustomer instance
         viewed_customer = RecentlyViewedCustomer.objects.create(user=user, customer_id=customer_id)
        # Delete the oldest RecentlyViewedCustomer if limit exceeded
        self.delete_oldest_if_exceeds_limit(user)
        # Serialize the created instance to return in the response
        serializer = RecentlyViewedCustomerSerializer(viewed_customer)
        # Return a successful response with the serialized data
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete_oldest_if_exceeds_limit(self, user):
        # Get the number of recently viewed customers for the user
        count = RecentlyViewedCustomer.objects.filter(user=user).count()
        # Check if the count exceeds the defined limit
        if count > self.MAX_RECENTLY_VIEWED:
            # Get the oldest RecentlyViewedCustomer instance
            oldest_viewed_customer = RecentlyViewedCustomer.objects.filter(user=user).order_by('viewed_at').first()
            # Delete the oldest RecentlyViewedCustomer instance
            if oldest_viewed_customer:
                print('delete:', oldest_viewed_customer)
                oldest_viewed_customer.delete()
    


    
    


