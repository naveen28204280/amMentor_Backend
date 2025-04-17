from django.db import models
from members.models import Members

# Create your models here.
class Tracks(models.Model):
    track=models.CharField(primary_key=True, default='Vidyaratna1')

class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    task_num = models.IntegerField()
    task_name = models.CharField(max_length=100)
    task_description=models.TextField(null=True)
    points=models.BigIntegerField()
    deadline=models.SmallIntegerField()

class Submissions(models.Model):
    member=models.ForeignKey(Members, on_delete=models.CASCADE, related_name='sub_member')
    mentor=models.ForeignKey(Members, on_delete=models.CASCADE, related_name='sub_mentor', null=True, blank=True)
    task=models.ForeignKey(Tasks, on_delete=models.CASCADE)
    sub_url=models.URLField() 
    pause_start=models.DateField(auto_now_add=True)
    pause_end=models.DateField(null=True)
    feedback=models.CharField(null=True, blank=True)
    accepted=models.BooleanField(null=True,blank=True)

class Curriculum(models.Model):
    member=models.ForeignKey(Members, on_delete=models.CASCADE, null=True, blank=True)
    task=models.ForeignKey(Tasks, on_delete=models.CASCADE)
    start=models.DateField(auto_now_add=True)
    end=models.DateField(null=True, blank=True)