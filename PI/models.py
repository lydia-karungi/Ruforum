from django.db import models
from contacts.models import User, Student
from django.utils import timezone
from grants.models import Grant


# Create your models here.


class ProjectEvent(models.Model):
    organiser = models.ForeignKey(User, models.DO_NOTHING, related_name="pi")
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name="grant")
    event_name = models.CharField(max_length=100, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    attendance = models.FileField(null=True, blank=True, help_text='Attach attendance list in excell format, if any.')
    event_description = models.TextField()
    photo_one = models.ImageField(null=True, blank=True)
    photo_two = models.ImageField(null=True, blank=True)
    photo_three = models.ImageField(null=True, blank=True)
    photo_four = models.ImageField(null=True, blank=True)
    photo_five = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.event_name
