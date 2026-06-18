from django.forms import ModelForm

from .models import Note, Job

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ('name','body', )


class JobCreationForm(ModelForm):
	class Meta:
		model = Job
		fields = ('name', 'lead', 'lead_two', )