from django.contrib import admin
from django.urls import include, path
from .models import *




urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]



admin.site.register(Customer, )
admin.site.register(Employee, )
admin.site.register(Organization, )
admin.site.register(User,  )



