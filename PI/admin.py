from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.
from PI.models import ProjectEvent

admin.site.register(ProjectEvent)
