from django.db import models
from organizers.models import Organizer, Workspace

# Create your models here.
class Poll(models.Model):

    seat = models.CharField(max_length=254, blank=False)
    intro = models.TextField()
    open = models.BooleanField(default=True, blank=False)
    begin_date = models.DateField()
    end_date = models.DateField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_date"]

        db_table = "Polls Table"

    def __str__(self) -> str:
        
        return self.seat

class Candidate(models.Model):

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254, blank=False)
    last_name = models.CharField(max_length=254, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    image = models.ImageField(upload_to='images/', blank=True)
    country = models.CharField(max_length=254, blank=False)
    bio = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_date"]

        db_table = "Poll Candidates"

    def __str__(self) -> str:
        
        return self.first_name