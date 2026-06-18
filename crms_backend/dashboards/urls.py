
from django.urls import path
from . import api
from .api import RecentlyViewedCustomerViewSet



urlpatterns = [
    path('<uuid:workerId>/lead_jobs/', api.lead_jobs ),

    path('recently_viewed_customers/<uuid:pk>/', RecentlyViewedCustomerViewSet.as_view({'delete': 'destroy', 'get': 'list', 'post': 'create',})),


    
]

