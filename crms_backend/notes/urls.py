
from django.urls import path
from . import api
from .api import NoteViewSet, JobViewSet



urlpatterns = [
    path('<uuid:customerId>/misc_note_create/', api.misc_note_create ),
    path('<uuid:customerId>/get_notes/', api.get_notes ),

    path('<uuid:customerId>/job_creation/', api.job_creation ),
    path('job_leads/', api.get_job_leads ),
    path('job_status/', api.get_job_status ),

    path('<uuid:customerId>/<uuid:jobId>/job_note_creation/', api.job_note_creation ),
    path('<uuid:customerId>/get_jobs/', api.get_jobs ),
    path('<uuid:customerId>/<uuid:jobId>/get_job_notes/', api.get_job_notes ),

    # path('<uuid:customerId>/update_job/<uuid:jobId>/', api.update_job ),


    path('notes/<uuid:pk>/', NoteViewSet.as_view({'delete': 'destroy', 'put': 'update',})),


    path('jobs/', JobViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('jobs/<uuid:pk>/', JobViewSet.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'})),



]

