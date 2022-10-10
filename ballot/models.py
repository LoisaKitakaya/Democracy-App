from django.db import models
from polls.models import Poll, Candidate
from voters.models import Voter

# Create your models here.
class Ballot(models.Model):

    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_date"]

        db_table = "Votes Table"

    def __str__(self) -> str:
        
        return f'Voter: {self.voter}, has voted for candidate: {self.candidate}, for poll: {self.poll}.'
