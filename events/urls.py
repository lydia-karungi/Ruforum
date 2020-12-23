from django.urls import path
from events.views import (
    EventsListView,
    CreateEventView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
)

app_name = 'events'


urlpatterns = [
    path('', EventsListView.as_view(), name='list'),
    path('create/', CreateEventView.as_view(), name='add_event'),
    path('<int:pk>/view/', EventDetailView.as_view(), name="view_event"),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name="edit_event"),
    path('<int:pk>/delete/',
         EventDeleteView.as_view(),
         name="remove_event"),
]
