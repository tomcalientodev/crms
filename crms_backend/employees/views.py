from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from accounts.models import Customer, Employee, OrganizationOwner, User, Note, Job
from employees.models import RecentlyViewed
from accounts.forms import NoteForm
from employees.forms import RecentlyViewedForm, JobForm
import json


#############
#SEARCH#####
############


# TODO: I have another search in the search app, maybe delete on of them?
def searchCustomers(request):
      if hasattr(request.user, 'employee'):
            emp_business = Employee.objects.filter(user = request.user).values('business_id')
      else:
            pass
      if hasattr(request.user, 'businessowner'):
            emp_business = OrganizationOwner.objects.filter(user = request.user).values('business_id')
      cust_business = Customer.objects.filter(business_id__in=emp_business).values('user_id')
      if request.method == 'GET':
            query = request.GET.get('search')
      if query == '':
            query =  'None'
      results = User.objects.filter( Q(first_name__icontains=query, id__in=cust_business) 
                                    | Q(last_name__icontains=query, id__in=cust_business)
                                    | Q(organization__icontains=query, id__in=cust_business))
      return render(request, 'employees/search_customers.html', {'query': query, 'results': results})
       

#####################################
#CUSTOMER PAGES for EMPLOYEES And OWNERS
####################################


def notes(request, id):
      """View for user to see Customer Page"""

      user = User.objects.get(id=id)
      note = Note.objects.filter(user_cust=id).order_by('note_updated_at') #for loop use filter. #TODO: maybe make the note stay at the top using async in the future.
      job = Job.objects.filter(user_cust_id=id)

      #Display's job leads: Filter for all employees/bizowners in logged on users Organization, then concatenate them.
      if hasattr(request.user, 'employee'):
            biz_id = Employee.objects.filter(user=request.user).values('business_id')
      else:
            no_objs = Employee.objects.none()  # Create an empty queryset
      if hasattr(request.user, 'businessowner'):
            biz_id = OrganizationOwner.objects.filter(user=request.user).values('business_id')
      else:
            no_objs = OrganizationOwner.objects.none()
      biz_leads = OrganizationOwner.objects.filter(Q(business_id__in=biz_id))
      emp_leads = Employee.objects.filter(Q(business_id__in=biz_id))
      all_leads = biz_leads.union(emp_leads)

      ##Adds Customer to Recently Viewed Form###
      recents =  RecentlyViewed.objects.filter(user_two = request.user.id)
      view = RecentlyViewedForm
      request.session['user_id'] = user.id
      try:
            form = RecentlyViewedForm(request.POST)
            if form.is_valid():
                  form.instance.user_id = id
                  form.instance.user_two = request.user.id
                  form.save()
      except:
            pass

      ###Limits Recently Viewed Entries and Deletes Them After Certain Amount.####
      number = len(RecentlyViewed.objects.filter(user_two=request.user.id))
      if number > 0:
            if number > 3:
                  x = RecentlyViewed.objects.order_by('created_at')[0]
                  # delete_qs = RecentlyViewed.objects.filter(created_at=max_date)
                  x.delete()
      else: 
            pass

      context = {
            'user': user,
            'note': note,
            'view': view,
            'recents': recents, 
            'job': job,
            'all_leads': all_leads,
      }
      return render(request,'employees/notes.html', context)



def save_note(request, id, user):
    """async htmx to let user know note was saved automatically"""
    if request.method == 'POST':
        note = NoteForm(request.POST)
        if note.is_valid():
            update = note.save(commit=False)
            Note.objects.filter(pk=id).update(cust_notes=update.cust_notes, 
                                              note_updated_at=datetime.now(), 
                                              updated_by=str(request.user))
            success_message = 'Note saved'
            return HttpResponse(success_message, content_type="text/plain")
        else:
            error_message = 'Form validation failed'
            return HttpResponse(error_message, status=400, content_type="text/plain")
    else:
        return HttpResponse('Invalid request method', status=405, content_type="text/plain")



#TODO: pre async-htmx to save note.
#TODO: Try using HTMX again to get message working using async: https://blog.benoitblanchon.fr/django-htmx-messages-framework/
# def save_note(request, id ,user):
#       if request.method == 'POST':
#             note = NoteForm(request.POST)
#             update = note.save(commit=False)
#             #Note.objects.filter(pk=id).update(cust_notes=update.cust_notes, note_updated_at=update.note_updated_at)
#             Note.objects.filter(pk=id).update(cust_notes=update.cust_notes, 
#                                               note_updated_at=datetime.now(), 
#                                               updated_by = str(request.user))
#             messages.success(request, "Your note is saved automatically!")
#             return HttpResponse(status=204)
#       else:
#            messages.error(request, "Try again, note not saved!")
#       return redirect('notes', user )


def employeeHomepage(request):
      emp = Employee.objects.filter(user = request.user)
      biz_owner = OrganizationOwner.objects.filter(user = request.user)
      recents =  RecentlyViewed.objects.filter(user_two = request.user.id)
      jobs = Job.objects.filter(Q(job_lead=request.user.id))
      quote_jobs = Job.objects.filter(job_lead_id=request.user.id, job_status="Quote")

      context = {
            'emp': emp,
            'biz_owner': biz_owner,
            'recents': recents,
            'jobs': jobs,
            'quote_jobs': quote_jobs,
      }
      return render(request, "employees/employee_homepage.html", context)



#TODO: Create a delete job button.
def job_creation(request, id):
      #TODO: Copy the same search feature in a separate function; let user select an employee lead.
      # Pass the lead's id to this function through querystring and attach it to the JobForm below.
      job_status_list = Job.JOB_STATUS
      form = JobForm()
      user = User.objects.get(id=id)
      jobs = Job.objects.filter(user_cust_id=id)
      #Queries for Employess in Users Organization for Dropdown menu to select job lead.
      if hasattr(request.user, 'employee'):
            emp_business = Employee.objects.filter(user = request.user).values('business_id')
      else:
            pass
      if hasattr(request.user, 'businessowner'):
            biz_business = OrganizationOwner.objects.filter(user = request.user).values('business_id')
      emp_business = Employee.objects.filter(business_id__in=biz_business).values('user_id')
      owner_business = OrganizationOwner.objects.filter(business_id__in=biz_business).values('user_id')
      results = User.objects.filter(Q(id__in=emp_business)|
                                    Q(id__in=owner_business ))
      #Form Submission
      if request.method == 'POST':
            job_form = JobForm(request.POST)
            if job_form.is_valid():
                  if hasattr(request.user, 'employee'): #TODO: can you add organization owner, so you only have one section?
                        job_form.instance.organization = request.user.employee.organization
                        job_form.instance.user_cust_id  = user.id
                        v2 = request.POST.get('job_lead')
                        job_form.instance.job_lead = v2
                        job_form.save()
                        job_id = job_form.instance.pk
                        messages.success(request, "You have created a New Job.")
                  elif hasattr(request.user, 'businessowner'):
                        job_form.instance.organization = request.user.businessowner.organization
                        job_form.instance.user_cust_id  = user.id
                        lead_job_id = request.POST.get('job_lead')
                        lead_job = User.objects.get(id=lead_job_id)
                        job_form.instance.job_lead = lead_job
                        job_form.save()
                        job_id = job_form.instance.pk
                        messages.success(request, "You have created a New Job.")
                  return redirect('jobnote-creation', id, job_id)
            else:
               messages.error(request, "Try creating a Customer Again something went wrong.")
      job_form = JobForm()
      context = {'job_form': job_form,
                 'results': results,
                 'user': user,
                 'jobs': jobs,
                 'job_status_list': job_status_list
                 }
      return render(request, "employees/job_creation.html", context )


def jobnote_creation(request,id, job_id):
      user = User.objects.get(id=id)
      jobs = Job.objects.filter(user_cust_id=id)
      name_job = get_object_or_404(Job, id=job_id)

      #Queries for Employess in Users Organization for Dropdown menu to select job lead.
      if hasattr(request.user, 'employee'):
            emp_business = Employee.objects.filter(user = request.user).values('business_id')
      else:
            pass
      if hasattr(request.user, 'businessowner'):
            biz_business = OrganizationOwner.objects.filter(user = request.user).values('business_id')
      emp_business = Employee.objects.filter(business_id__in=biz_business).values('user_id')
      owner_business = OrganizationOwner.objects.filter(business_id__in=biz_business).values('user_id')
      results = User.objects.filter(Q(id__in=emp_business)|
                                    Q(id__in=owner_business ))
      #Form Submission
      if request.method == 'POST':
            customer_form = NoteForm(request.POST)
            if customer_form.is_valid():
                  if hasattr(request.user, 'employee'): #TODO: can you add organization owner, so you only have one section?
                        customer_form.instance.user_cust_id = user.id
                        customer_form.instance.note_by = str(request.user)
                        customer_form.instance.organization = request.user.employee.organization
                        customer_form.instance.note_created_at = datetime.now()
                        customer_form.instance.related_job_id = job_id 
                        customer_form.save()
                        messages.success(request, "You have created a New Note.")
                  elif hasattr(request.user, 'businessowner'):
                        customer_form.instance.user_cust_id = user.id
                        customer_form.instance.organization = request.user.businessowner.organization
                        customer_form.instance.note_by = str(request.user)
                        customer_form.instance.note_created_at = datetime.now()
                        customer_form.instance.related_job_id = job_id
                        customer_form.save()
                        messages.success(request, "You have created a New Note.")
                  return redirect('notes',id)
            else:
               messages.error(request, "Try creating a Customer Again something went wrong.")
      customer_form = NoteForm()
      context = {'customer_form': customer_form,
                 'results': results,
                 'user': user,
                 'jobs': jobs,
                 'name_job': name_job,
                 }
      return render(request, "employees/jobnote_creation.html", context )



#TODO: Add the option to link the note to a job, by having the user select a job or None.
def create_misc_note(request, id):
      customer = User.objects.get(pk=id)
      user = User.objects.get(pk=id) #TODO: Cleaner code: change all of these user's to customers. User usually means logged on user.
     # emp_business = Employee.objects.filter(user = request.user).values('business_id')
      #cust_business = Customer.objects.filter(business_id__in=emp_business).values('user_id')
      #names = User.objects.all()
      if request.method =="POST":
            customer_form = NoteForm(request.POST)
            if customer_form.is_valid():
                  if hasattr(request.user, 'employee'):
                        customer_form.instance.user_cust_id = user.id
                        customer_form.instance.note_by = str(request.user)
                        customer_form.instance.organization = request.user.employee.organization
                        customer_form.instance.note_created_at = datetime.now()
                        note_name = 'Free Note'
                        customer_form.instance.note_name = note_name
                        customer_form.save()
                        messages.success(request, "You have created a customer note.")
                  if hasattr(request.user, 'businessowner'):
                        customer_form.instance.user_cust_id = user.id
                        customer_form.instance.organization = request.user.businessowner.organization
                        customer_form.instance.note_by = str(request.user)
                        customer_form.instance.note_created_at = datetime.now()
                        note_name = 'Free Note'
                        customer_form.instance.note_name = note_name
                        customer_form.save()
                        messages.success(request, "You have created a customer note.")
            else:
               messages.error("Try creating a Customer Again something went wrong.")
            return redirect('notes', user.id)
      customer_form = NoteForm()
      return render(request, "employees/create_note.html", context={"customer_form": customer_form, 'customer': customer, } )



def delCustomerNote(request, id):
      form = Note.objects.get(pk=id)
      if request.method == "POST":
            form.delete()
            messages.success(request, 'Customer Note Deleted')
            return redirect("notes", form.user_cust_id)
      return render(request, 'employees/del_customer_note.html', {'form':form})


def jobs(request, id):
      """Lists all Jobs, Leads, and Status to edit"""
      user = User.objects.get(pk=id)
      jobs = Job.objects.filter(user_cust_id=id)
      #Filter for all employees/bizowners in logged on users Organization, ten concatenate them.
      if hasattr(request.user, 'employee'):
            biz_id = Employee.objects.filter(user=request.user).values('business_id')
      else:
            no_objs = Employee.objects.none()  # Create an empty queryset
      if hasattr(request.user, 'businessowner'):
            biz_id = OrganizationOwner.objects.filter(user=request.user).values('business_id')
      else:
            no_objs = OrganizationOwner.objects.none()
      biz_leads = OrganizationOwner.objects.filter(Q(business_id__in=biz_id))
      emp_leads = Employee.objects.filter(Q(business_id__in=biz_id))
      all_leads = biz_leads.union(emp_leads)

      # #Change and save the newly selected lead.
      # name = request.POST.get('job_name') # Now you need to ge the id of the job name.
      # id_job = Job.objects.filter(Q(job_lead_id=name))
      # lead = request.POST.get('job_lead')
      # #TODO:It should have the job_id below not the customer id. That is an issue.
      # if request.method =="POST":
      #       Job.objects.update(job_lead=lead)
      return render(request, "employees/jobs.html", {'jobs': jobs, 'user': user, 'all_leads': all_leads, })



def update_job(request):
    if request.method == "POST":
      #Save Job Lead Change.
      job_id = request.POST.get('job_id')
      job_lead_id = request.POST.get('job_lead')
      job = Job.objects.get(id=job_id)
      job_lead = User.objects.get(id=job_lead_id)
      job.job_lead = job_lead
      #Save job Status Change
      status = request.POST.get('job_status')
      job.job_status = status
      job.save()
      messages.success(request, 'Change Saved')
    return redirect('jobs', job.user_cust_id)



def job_notes(request, cust_id, job_id):
      user = User.objects.get(pk=cust_id)
      note = Note.objects.filter(related_job_id=job_id)
      job = Job.objects.get(id=job_id)
      return render(request, "employees/job_notes.html", {'note': note, 'user': user, 'job': job,})




def fetch_messages(request):
    """uses async to fetch django message and make them async. Problem is I want this separate from Django messages."""
    print("fetch_messages view called")
    print(request.method)
    print(request.GET)
    message_list = []
    for message in messages.get_messages(request):
        message_list.append({
            'level': message.level,
            'message': message.message,
        })
    return JsonResponse(message_list, safe=False)



###########################

#TODO: Try @transaction.atomic (commit on success) to fix this autosave issue.
#Auto-Saves Note Field in Dashboard
# def customer_note_endpoint(request):
#       if request.method == 'POST':
#             # When receiving json from Fetch API or "ajax", you get the data from request.body
#             # To convert that json data into Python, import json and wrap request.body with json.loads
#             data = json.loads(request.body)
#             user_cust_id = int(data['user_cust_id'])
#             customer_note_text = data['cust_notes']
#             print('Note text:', customer_note_text)
#             # Get user
#             note = Note.objects.get(user_cust_id=user_cust_id)
#             # Update their note text
#             print('Old note text:', note.cust_notes)
#             note.cust_notes = customer_note_text
#             note.save()
#             print('New note text:', note.cust_notes)
#             # Save to the database
#             note.save()
#             return JsonResponse({'message': 'Post successful!'})
#       return JsonResponse({'message': 'Invalid method'}, status=405)



######################################################################

#Combo of Note form and job form in one. Got rid of this feature.
# def job_creation(request, id):
#       #TODO: Copy the same search feature in a separate function; let user select an employee lead.
#       # Pass the lead's id to this function through querystring and attach it to the JobForm below.
#       form = JobForm()
#       user = User.objects.get(id=id)
#       jobs = Job.objects.filter(user_cust_id=id)
#       #Queries for Employess in Users Organization for Dropdown menu to select job lead.
#       if hasattr(request.user, 'employee'):
#             emp_business = Employee.objects.filter(user = request.user).values('business_id')
#       else:
#             pass
#       if hasattr(request.user, 'businessowner'):
#             biz_business = OrganizationOwner.objects.filter(user = request.user).values('business_id')
#       emp_business = Employee.objects.filter(business_id__in=biz_business).values('user_id')
#       owner_business = OrganizationOwner.objects.filter(business_id__in=biz_business).values('user_id')
#       results = User.objects.filter(Q(id__in=emp_business)|
#                                     Q(id__in=owner_business ))
#       #Form Submission
#       if request.method == 'POST':
#             job_form = JobForm(request.POST)
#             customer_form = NoteForm(request.POST)
#             if job_form.is_valid() and customer_form.is_valid():
#                   if hasattr(request.user, 'employee'): #TODO: can you add organization owner, so you only have one section?
#                         job_form.instance.organization = request.user.employee.organization
#                         job_form.instance.user_cust_id  = user.id
#                         customer_form.instance.user_cust_id = user.id
#                         customer_form.instance.note_by = str(request.user)
#                         customer_form.instance.organization = request.user.employee.organization
#                         customer_form.instance.note_created_at = datetime.now()
#                         v2 = request.POST.get('job_lead')
#                         job_form.instance.job_lead = v2
#                         job_form.save()
                        
#                         new_job_id = job_form.instance.pk #Get the id of the job form just saved in the DB.
#                         customer_form.instance.related_job_id = new_job_id #attach the job form's id to the note class.
                        
#                         customer_form.save()
#                         messages.success(request, "You have created a New Job and Note.")
#                   elif hasattr(request.user, 'businessowner'):

#                         job_form.instance.organization = request.user.businessowner.organization
#                         job_form.instance.user_cust_id  = user.id

#                         v2 = request.POST.get('job_lead')
#                         job_form.instance.job_lead = v2

#                         job_form.save()
                        
#                         new_job_id = job_form.instance.pk #Get the id of the job form just saved in the DB.
#                         customer_form.instance.related_job_id = new_job_id #attach the job form's id to the note class.
                        
#                         customer_form.instance.user_cust_id = user.id
#                         customer_form.instance.organization = request.user.businessowner.organization
#                         customer_form.instance.note_by = str(request.user)
#                         customer_form.instance.note_created_at = datetime.now()
#                         customer_form.save()
#                         messages.success(request, "You have created a New Job and Note.")
#                   return redirect('notes',id )
#             else:
#                messages.error(request, "Try creating a Customer Again something went wrong.")
#       customer_form = NoteForm()
#       job_form = JobForm()
#       context = {'job_form': job_form,
#                  'customer_form': customer_form,
#                  'results': results,
#                  'user': user,
#                  'jobs': jobs,
#                  }
#       return render(request, "employees/job_creation.html", context )