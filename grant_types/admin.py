from django.contrib import admin
from grant_types.models import Granttype
from reversion.admin import VersionAdmin

admin.site.register(Granttype)
