from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import (
    Fellowshipapplication,Fellowshipappreview
)

admin.site.register(Fellowshipapplication)
admin.site.register(Fellowshipappreview)