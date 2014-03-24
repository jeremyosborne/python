from django.shortcuts import render

from notes.models import Note

def index(request):
    context = {
        # Get all of the notes in the database, in descending order.
        # Instead of SQL, this is how Django provides a cross-database
        # query engine.
        'notes': Note.objects.all().order_by('-date')
    }
    # Map our context object that we just built, with all of our models,
    # into our template. Whatever the results will be passed back as
    # the response to this particular HTTP request.
    return render(request, 'notes/index.html', context)



# CHANGEME: Class based instead of functional based view.
from django import forms

# A form that excludes fields we want to populate ourself via session data.
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('author','date',)

# We only allow creation of notes.
from datetime import datetime
from django.views.generic.edit import CreateView

class NoteCreate(CreateView):
    form_class = NoteForm
    model = Note
    template_name = 'notes/add.html'
    success_url = '/'
    
    def form_valid(self, form):
        # Populate the information ourselves that was excluded.
        form.instance.author = self.request.user
        form.instance.date = datetime.now()
        # Delegate validation to parent class.
        return super(NoteCreate, self).form_valid(form)
