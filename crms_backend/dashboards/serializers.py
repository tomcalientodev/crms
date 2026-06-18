from rest_framework import serializers
from .models import RecentlyViewedCustomer
from accounts.serializers import CustomerSerializer, UserSerializer



class RecentlyViewedCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer() #already have UserSerializer in CustomerSerializer, so you will ge the customer info returned.
    class Meta:
        model = RecentlyViewedCustomer
        fields = ['id', 'customer', 'viewed_at']
