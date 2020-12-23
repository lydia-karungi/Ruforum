from django.urls import path
from project_management.views import (
    ProjectListView,
    CreateProjectView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    SelectProjectView,
    ProjectaActivitiesListView,
    CreateFrameworkView,
    FrameworkDetailView,
    FrameworkDeleteView,
    FrameworkUpdateView,


)
app_name = 'project_management'

urlpatterns = [
    path('', ProjectListView.as_view(), name='projectlist'),
    path('activitieslist', ProjectaActivitiesListView.as_view(), name='activitieslist'),

    path('create_project', CreateProjectView.as_view(), name='create_project'),
    path('create_framework', CreateFrameworkView.as_view(), name='create_framework'),
    path('<int:pk>/view_project/', ProjectDetailView.as_view(), name="view_project"),
    path('<int:pk>/edit_project/', ProjectUpdateView.as_view(), name="edit_project"),
    path('<int:pk>/delete_project/', ProjectDeleteView.as_view(), name="delete_project"),
    path('select_project/', SelectProjectView.as_view(), name='select_project'),
    path('<int:pk>/view_framework/', FrameworkDetailView.as_view(), name="view_framework"),
    path('<int:pk>/edit_project_framework/', FrameworkUpdateView.as_view(), name="edit_project_framework"),
    path('<int:pk>/delete_project_framework/', FrameworkDeleteView.as_view(), name="delete_project_framework"),
]
