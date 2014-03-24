from django.db import models
# CHANGEME: Notes models need authors.
from django.contrib.auth.models import User
# CHANGME: To auto set dates.
from datetime import datetime

class Note(models.Model):
    """A single note on our bulletin board.
    """
    # Not shown: all models have an id field by default.
    # Who wrote the note.
    author = models.ForeignKey(User)
    # When the note was written, defaulting to the callback now.
    date = models.DateField('creation date', default=datetime.now)
    # All notes must have unique titles.
    title = models.CharField(max_length=200, unique=True, help_text='Each note title must be unique.')
    # The body of the note.
    body = models.TextField(help_text='Write as much as you want.')
