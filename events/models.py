from django.db import models

from contacts.models import User


class Event(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    host_city = models.CharField(max_length=256)
    organizer = models.TextField()
    partners = models.TextField()
    participants = models.ManyToManyField(User)

    class Meta:
        ordering = ['start_date']


