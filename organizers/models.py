from django.db import models
from users.models import User

# Create your models here.
class Organizer(models.Model):

    FREE = 'FREE_TIER'
    PRO = 'PRO_TIER'
    BUSINESS = 'BUSINESS_TIER'
    ENTERPRISE = 'ENTERPRISE_TIER'

    PRODUCT_PACKAGES = (
        (FREE, 'free tier'),
        (PRO, 'pro tier'),
        (BUSINESS, 'business tier'),
        (ENTERPRISE, 'enterprise tier'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    phone = models.CharField(max_length=254, blank=False)
    country = models.CharField(max_length=254, blank=False)
    paid_status = models.BooleanField(default=False, verbose_name="has purchased a package")
    running_package = models.CharField(max_length=30, choices=PRODUCT_PACKAGES, default=FREE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_date"]

        db_table = "Poll Organizers"

    def __str__(self) -> str:
        
        return self.user.username

class Workspace(models.Model):

    name = models.CharField(max_length=254, blank=False)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    voter_limit = models.IntegerField(default=10, blank=False)
    poll_limit = models.IntegerField(default=1, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_date"]

        db_table = "Workspaces"

    def __str__(self) -> str:
        
        return self.name