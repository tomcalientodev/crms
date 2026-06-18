from django.urls import path
from . import api


urlpatterns = [
    path('', api.search, name='search' ),
    path('all_customers', api.all_customers,),
]