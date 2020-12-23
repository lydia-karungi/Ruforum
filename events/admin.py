from django.contrib import admin
from .models import Event
from reversion.admin import VersionAdmin

'''
class EventParticipantsInline(admin.TabularInline):
    model = EventParticipants
'''

class EventParticipantsInline(admin.TabularInline):
    model = Event.participants.through


class EventAdmin(VersionAdmin,admin.ModelAdmin):
    list_display = [
        'title',
        'start_date',
        'end_date',
        'host_city',
        'organizer',
        'partners',
    ]
    inlines = [
        EventParticipantsInline
    ]
    exclude = ('participants',)

admin.site.register(Event, EventAdmin)