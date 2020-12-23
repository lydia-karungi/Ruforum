from django.urls import path, include
from contacts.views import (
    ContactsListView,
    CreateContactView,
    ContactDetailView,
    UpdateContactView,
    ContactDeleteView,
    StudentsListView,
    CreateStudentView,UpdateStudentView,StudentDeleteView,GraduateStudentView,StudentDetailView,
    ContactViewSet
)
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.ContactViewSet,basename="contacts")

app_name = 'contacts'


urlpatterns = [
    path('api/', include(router.urls)),
    path('', ContactsListView.as_view(), name='list'),
    path('create/', CreateContactView.as_view(), name='add_contact'),
    path('<int:pk>/Details/', ContactDetailView.as_view(), name="contact_details"),
    path('<int:pk>/edit/', UpdateContactView.as_view(), name="edit_contact"),
    path('<int:pk>/delete/', ContactDeleteView.as_view(), name="remove_contact"),


    #students
    path('students/list/', StudentsListView.as_view(), name='students_list'),
    path('students/create/', CreateStudentView.as_view(), name='add_student'),
    path('<int:pk>/student/edit/', UpdateStudentView.as_view(), name='edit_student'),
    path('<int:pk>/student/delete/', StudentDeleteView.as_view(), name="remove_contact"),
    path('<int:pk>/student/graduate/<slug:grad_actual>/', GraduateStudentView.as_view(), name="graduate_student"),
    path('student/<int:pk>/Details/', StudentDetailView.as_view(), name="student_details"),
]
