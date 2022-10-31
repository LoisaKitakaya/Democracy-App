from django.db import models
from users.models import User
from organizers.models import Workspace

# Create your models here.
class Voter(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=254, blank=False, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='voters/', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_date"]

        db_table = "Poll Voters"

    def __str__(self) -> str:
        
        return self.user.username