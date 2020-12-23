from django.urls import path,include
from PI.views import (
    StudentsListView,
    CreateEnrollmentView,
    EnrolledStudentsListView,
    UnRollView,
    PIReportsListView,
    ApplicantListView, CreatePIStudentView, GrantsListView, ProjectEventCreateView, ProjectEventListView,
    ProjectEventUpdateView, DeleteProjectEventView, ProjectEventDetailView,UpdatePIStudentView

)
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'applicants', views.ApplicantsViewSet)


app_name = 'PI'



urlpatterns = [
    path('api/', include(router.urls)),
    path('students', StudentsListView.as_view(), name='student_list'),
    path('student/enrollment/', CreateEnrollmentView.as_view(), name='enroll_student'),
    path('students/enrolled', EnrolledStudentsListView.as_view(), name="enrolled_students"),
    path('create/project_event', ProjectEventCreateView.as_view(), name="create_project_event"),
    path('<int:pk>/unroll/', UnRollView.as_view(), name="unroll_student"),
    path('project/events', ProjectEventListView.as_view(), name="events"),
    path('<int:pk>/project_event/edit', ProjectEventUpdateView.as_view(), name="edit_project_event"),
    path('<int:pk>/delete/event/', DeleteProjectEventView.as_view(), name="delete_project_event"),
    path('<int:pk>/view/event/', ProjectEventDetailView.as_view(), name="view_project_event"),
    path('applicants', ApplicantListView.as_view(), name='applicant_list'),
    path('<int:user_pk>/enroll_applicant/', CreatePIStudentView.as_view(), name="create_pi_studemt"),
    path('grants', GrantsListView.as_view(), name='pi_grant_list'),
    path('reports', PIReportsListView.as_view(), name="reports"),
    path('<int:pk>/edit/student/', UpdatePIStudentView.as_view(), name="edit_pi_student"),

]
