
from django.urls import path
from . import views




urlpatterns = [

    path('search_customers', views.searchCustomers, name="search-customers"),

    path('notes/<id>', views.notes, name='notes'),
    path('jobs/<id>/', views.jobs, name='jobs'),
    path('job_notes/<int:cust_id>/<int:job_id>', views.job_notes, name='job-notes'),
    #path('jobnotes/<id>/', views.jobnotes, name='jobnotes'), uncreated

    path('employee_homepage', views.employeeHomepage, name='employee-homepage'),
    
    path('del_customer_note/<id>', views.delCustomerNote, name='del-customer-note'),
    path('save_note/<id>/<user>', views.save_note,name='save-note'),
    path('update_job', views.update_job, name='update-job'),
    


    path('jobnote_creation/<int:id>/<int:job_id>', views.jobnote_creation, name='jobnote-creation'),
    path('job_creation/<int:id>', views.job_creation, name='job-creation'),
    path('create_misc_note/<int:id>/', views.create_misc_note, name='create-misc-note'),

    path('fetch_messages', views.fetch_messages, name='fetch-messages'),
    

    # path('clear_success_message', views.clear_success_message, name='clear-success-message'),

    #path('recently_viewed', views.recently_viewed, name='recently-viewed')
    # path('customers/notes/', views.customer_note_endpoint,name='customer_note_endpoint'), #Autosaves note.

]

htmx_urlpatterns = [



]

urlpatterns += htmx_urlpatterns

