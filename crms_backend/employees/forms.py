from django import forms
from .models import RecentlyViewed
from accounts.models import Job, User, OrganizationOwner


class RecentlyViewedForm(forms.ModelForm):
	class Meta:
		model = RecentlyViewed
		fields = ('user_two',)


class JobForm(forms.ModelForm):
	
	class Meta:
		model = Job
		fields = ('job_name', 'job_lead', 'job_status', )
