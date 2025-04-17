from django.db import models
from members.models import Members

# Create your models here.
class Badges(models.Model):
    badge=models.CharField(primary_key=True)
    icon=models.URLField(null=True, blank=True )

class Badges_Members(models.Model):
    member=models.ForeignKey(Members, on_delete=models.SET_NULL, null=True, blank=True)
    badge=models.ForeignKey(Badges, on_delete=models.SET_NULL, null=True, blank=True)
    description=models.CharField()