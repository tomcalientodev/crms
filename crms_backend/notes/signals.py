from django.db.models.signals import pre_delete
from django.dispatch import receiver



@receiver(pre_delete, sender='notes.Job')  # Use string for sender to avoid direct import
def delete_related_notes(sender, instance, **kwargs):
    from notes.models import Note  # Import Note where it's needed
    # Delete all notes related to the instance (job being deleted)
    Note.objects.filter(related_job=instance).delete()