from django.db import models
from contacts.models import User
#from accounts.models import Account
#from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _

from hrm.models import StaffProfile


class Task(models.Model):
    STATUS_CHOICES = (
        (None, '--please select--'),
        ('not_started', 'Not started'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'))

    PRIORITY_CHOICES = (
        (None, '--please select--'),
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    )

    title = models.CharField(_("title"), max_length=200)
    status = models.CharField(
        _("status"), max_length=50, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(
        _("priority"), max_length=50, choices=PRIORITY_CHOICES)
    due_date = models.DateField(blank=True, null=True)
    from_date = models.DateTimeField(blank=False, null=True)
    new_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ManyToManyField(StaffProfile, related_name='users_tasks')

    created_by = models.ForeignKey(
        User, related_name='task_created', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-due_date']
