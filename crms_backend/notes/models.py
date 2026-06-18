from django.db import models
import uuid
from django.utils.timesince import timesince
from accounts.models import Customer, Employee, User, Organization
from notes.signals import delete_related_notes



class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, blank=True, null=True)
    body = models.CharField(max_length=1000, blank=True, null=True)

    related_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    related_job = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_notes', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return timesince(self.created_at)


class Job(models.Model):

    JOB_STATUS =(
        ("Job Created", "Job Created"),
        ("Call Back", "Call Back"),
        ("Needs Quote", " Needs Quote"),
        ("In Progress", "In Progress"),
        ("Payment Needed", "Payment Needed"),
        ("Paid/Job Complete", "Paid/Job Complete"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True, choices = JOB_STATUS, default="Job Created")
    lead = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, max_length=50, related_name='job_lead')
    lead_two = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, max_length=50, related_name='job_lead_two')
    due_date = models.DateField(null=True, blank=True)

    related_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='job_customer')
    related_organization = models.ForeignKey(Organization,  on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)
