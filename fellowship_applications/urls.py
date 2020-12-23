from django.urls import path, include
from fellowship_applications.views import (
    FellowshipapplicationsListView,
    FellowshipapplicationsValidationListView,
    FellowshipapplicationsReviewListView,
    CreateFellowshipapplicationView,
    FellowshipapplicationDetailView,
    FellowshipapplicationUpdateView,
    AssignFellowshipValidatorsView,
    FellowshipapplicationDeleteView,
    AddFellowshipappreviewView,
    UpdateFellowshipappreviewView,
    DeleteFellowshipappreviewView,
    FellowshipapplicationReviewersView,
    FellowshipapplicationsReviewedListView,FellowshipapplicationDecisionView,
    FellowshipapplicationReview,SelectCallView,SaveFellowshipapplicationReviewersView,
    FellowshipapplicationValidatorsView,FellowshipapplicationValidateView,

)

from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
router = routers.DefaultRouter()
router.register(r'applications', views.FellowshipApplicationViewSet, basename='fellowshipapplication')
router.register(r'validation/list',views.FellowshipApplicationValidationViewSet, basename='FellowshipapplicationValidation')
router.register(r'validated/applications', views.ValidatedFellowshipViewSet, basename='validated_applications')
router.register(r'application/reviewed', views.ReviewedViewSet, basename='FellowshipApplicationReview')

app_name = 'fellowship_applicationss'


urlpatterns = [
    path('api/', include(router.urls)),
    path('', FellowshipapplicationsListView.as_view(), name='list'),
    path('select_call/', SelectCallView.as_view(), name='select_fellowship_call'),
    path('validation_list', FellowshipapplicationsValidationListView.as_view(), name='validation_list'),
    path('review_list', FellowshipapplicationsReviewListView.as_view(), name='review_list'),
    path('reviewed_list',FellowshipapplicationsReviewedListView.as_view(), name="reviewed_list"),
    path('create/<int:call_pk>', CreateFellowshipapplicationView.as_view(), name='add_application'),
    path('<int:pk>/view/', FellowshipapplicationDetailView.as_view(), name="view_application"),
    path('<int:pk>/review/', FellowshipapplicationReview.as_view(), name="review_application"),
    path('<int:pk>/edit/', FellowshipapplicationUpdateView.as_view(), name="edit_application"),
    path('<int:pk>/validate/application', FellowshipapplicationValidateView.as_view(), name="validate_fellowship_application"),
    path('assign-reviewers/', FellowshipapplicationReviewersView.as_view(), name="assign_reviewers"),
    path('<int:pk>/delete/', FellowshipapplicationDeleteView.as_view(), name="remove_application"),
    path('assign-validators/',FellowshipapplicationValidatorsView.as_view(),name="assign_validators"),
    path('save_fellowship_validators/', AssignFellowshipValidatorsView.as_view(), name="save_fellowship_validators"),
    path('save-reviewers/', SaveFellowshipapplicationReviewersView.as_view(), name="save-reviewer"),
    path('review/add/', AddFellowshipappreviewView.as_view(), name="add_review"),
    path('review/edit/', UpdateFellowshipappreviewView.as_view(), name="edit_review"),
    path('review/remove/',
         DeleteFellowshipappreviewView.as_view(),
         name="remove_review"),
    path('<int:pk>/decision/', FellowshipapplicationDecisionView.as_view(), name="application_decision"),



]
