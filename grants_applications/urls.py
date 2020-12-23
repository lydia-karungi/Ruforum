from django.urls import path,include
from grants_applications.views import (
    GrantapplicationsListView,
    GrantapplicationsValidationListView,
    GrantapplicationsReviewListView,
    CreateGrantapplicationView,
    GrantapplicationDetailView,
    GrantapplicationUpdateView,
    GrantapplicationValidateView,
    GrantapplicationDeleteView,
    AddGrantappreviewView,
    UpdateGrantappreviewView,
    DeleteGrantappreviewView,
    GrantapplicationReviewersView,
    GrantapplicationsReviewedListView, GrantCarpapplicationReview,
    GrantapplicationReview, SelectCallView, GrantapplicationValidatorsView, GrantapplicationsValidatedListView
, GrantapplicationRejectView, GrantapplicationsDecisionListView, AssignValidatorsView, AssignGrantReviewersListView
,
)
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'applications', views.GrantApplicationViewSet, basename='Grantapplication')
router.register(r'validation/list',views.GrantApplicationValidationViewSet, basename='GrantapplicationValidation')
router.register(r'application/decision', views.GrantApplicationDecisionViewSet, basename='GrantApplicationDecision')
router.register(r'application/reviewed', views.ReviewedViewSet, basename='GrantApplicationReview')

app_name = 'grants_applicationss'


urlpatterns = [
    path('api/', include(router.urls)),
    path('', GrantapplicationsListView.as_view(), name='list'),
    path('validation_list', GrantapplicationsValidationListView.as_view(), name='validation_list'),
    path('validated_list', GrantapplicationsValidatedListView.as_view(), name='validated_list'),
    path('review_list', GrantapplicationsReviewListView.as_view(), name='review_list'),
    path('reviewed_list', GrantapplicationsReviewedListView.as_view(), name="reviewed_list"),
    path('create/<int:call_pk>', CreateGrantapplicationView.as_view(), name='add_application'),
    path('<int:pk>/view/', GrantapplicationDetailView.as_view(), name="view_application"),
    path('<int:pk>/review/', GrantapplicationReview.as_view(), name="review_application"),
    path('<int:pk>/review/carp', GrantCarpapplicationReview.as_view(), name="review_carp_application"),
    path('<int:pk>/edit/', GrantapplicationUpdateView.as_view(), name="edit_application"),
    path('<int:pk>/validate/', GrantapplicationValidateView.as_view(), name="validate_application"),
    path('assign-reviewers/', AssignGrantReviewersListView.as_view(), name="assign_reviewers"),
    path('assign-validators/', GrantapplicationValidatorsView.as_view(),name="assign_validators"),
    path('save-validators/', AssignValidatorsView.as_view(), name="save_validators"),
    path('save-reviewers/', GrantapplicationReviewersView.as_view(), name="save-reviewer"),
    path('<int:pk>/delete/', GrantapplicationDeleteView.as_view(), name="remove_application"),
    path('select_call/', SelectCallView.as_view(), name='select_grant_call'),
    path('<int:pk>/reject', GrantapplicationRejectView.as_view(), name="reject_grant_application"),

    path('review/add/', AddGrantappreviewView.as_view(), name="add_review"),
    path('review/edit/', UpdateGrantappreviewView.as_view(), name="edit_review"),
    path('review/remove/',
         DeleteGrantappreviewView.as_view(),
         name="remove_review"),
    path('application/decision', GrantapplicationsDecisionListView.as_view(), name="application_decision_list"),
    
]
