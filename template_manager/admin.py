from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Template


class TemplateAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'model',
        'field_name',
        'label',
        'file',
    ]
   

admin.site.register(Template, TemplateAdmin)
