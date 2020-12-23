from django.urls import path
from student_reports.views import (
    StudentreportsListView,
    CreateStudentreportView,
    StudentreportDetailView,
    StudentreportUpdateView,
    StudentreportDeleteView,
    MyStudentreportsListView,
    SingleStudentreportsListView
)

app_name = 'student_reports'

urlpatterns = [
    path('', StudentreportsListView.as_view(), name='list'),
    path('my_reports', MyStudentreportsListView.as_view(), name='my_reports'),
    path('student/reports', SingleStudentreportsListView.as_view(), name='my_student_reports'),
    path('<period>/create/', CreateStudentreportView.as_view(), name='add_student_report'),
    path('<int:pk>/view/', StudentreportDetailView.as_view(), name="view_student_report"),
    path('<int:pk>/edit/', StudentreportUpdateView.as_view(), name="edit_student_report"),
    path('<int:pk>/delete/',
         StudentreportDeleteView.as_view(),
         name="remove_student_report"),
]
