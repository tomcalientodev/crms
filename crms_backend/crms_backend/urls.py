from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('api/notes/', include('notes.urls')),
    path('api/dashboards/', include('dashboards.urls')),
    path('api/search/', include('search.urls')),
    #path('', include('django.contrib.auth.urls')), 
    path('admin/', admin.site.urls),

] 
