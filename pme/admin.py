from django.contrib import admin
from .models import Expectedoutput,Activity,Indicator,ActivityOutput,FrameWorkUnit
from reversion.admin import VersionAdmin
# Register your models here.
admin.site.register(Expectedoutput)
admin.site.register(Activity)
admin.site.register(Indicator)
admin.site.register(ActivityOutput)
admin.site.register(FrameWorkUnit)