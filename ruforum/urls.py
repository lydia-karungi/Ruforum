"""ruforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import include

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls', namespace="tasks")),
    path('', include('common.urls', namespace="common")),
    path('', include('django.contrib.auth.urls')),
    path('contacts/', include('contacts.urls', namespace="contacts")),
    path('calls/', include('calls.urls')),
    path('grantapplications/', include('grants_applications.urls', namespace="grants_applications")),
    path('scholarships/', include('scholarships.urls', namespace="scholarships")),
    path('grants/', include('grants.urls')),
    path('grant_types/', include('grant_types.urls', namespace="grant_types")),
    path('fellowship/', include('fellowship.urls')),
    path('fellowshipapplications/', include('fellowship_applications.urls', namespace="fellowship_applications")),
    path('template_manager/', include('template_manager.urls', namespace="template_manager")),
    path('events/', include('events.urls', namespace="events")),
    path('student_reports/', include('student_reports.urls', namespace="student_reports")),
    path('grants_reports/', include('grants_reports.urls', namespace="grants_reports")),
    path('hrm/', include('hrm.urls', namespace="hrm")),
    path('pme/', include('pme.urls', namespace="pme")),
    path('PI/', include('PI.urls', namespace="PI")),
    path('project_management/', include('project_management.urls', namespace="project_management")),

    #path('passwordrest',auth_views.PasswordResetView.as_view(), name='passwordrest'),
    path('passwordrest/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('passwordrest/complete',auth_views.PasswordResetCompleteView.as_view(), name='passwordrest'),
    path('session_security/', include('session_security.urls')),
    #path('accounts/login/', auth_views.LoginView.as_view()),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('comments/', include('django_comments.urls')),
]
