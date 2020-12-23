from django.urls import path, include
from scholarships.views import (
    ScholarshipsListView,
    ScholarshipsReviewListView,
    MastercardReviewListView,
    CreateScholarshipView,
    CreateMastercardScholarshipView,
    UpdateScholarshipView,
    UpdateMastercardScholarshipView,
    ScholarshipapplicationDetailView,
    AddReviewView,
    SelectCallView,
    ScholarshipReviewReportView,
    ScholarshipapplicationDeleteView,
    ReviewedScholorshipListView,EditScholarshipView,AwardedScholarshipDetailView,
    ScholarshipapplicationReviewView, CreatScholarReviewerView, ScholarshipapplicationRewiewDetailView,
    UpdateScholarshipView, AssignReviewerView, ScholarshipPrintView, CreateScholarshipApprovalView,
    ScholarshipApplicationRejectView, ScholarshipsApplicationDecisionListView, AwardedScholarshipsListView,
    ScholarshipValidatorsView, AssignScholarshipValidatorsView, ScholarshipValidationListView,
    ScholarshipapplicationValidationView, ScholarshipApplicationValidateView
)

from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'scholarships', views.ScholarshipViewSet, basename='scholarships')
app_name = 'scholarships'


urlpatterns = [
    path('api/', include(router.urls)),
    path('', ScholarshipsListView.as_view(), name='list'),
    path('review_list', MastercardReviewListView.as_view(), name='mastercard_review_list'),
    path('assign-validators/', ScholarshipValidatorsView.as_view(), name="assign_application_validators"),
    path('save-scholarship-validators/', AssignScholarshipValidatorsView.as_view(), name="save_scholarship_validators"),
    path('reviewed/list', ReviewedScholorshipListView.as_view(), name='reviewed_scholarships_list'),
    path('review_list_s', ScholarshipsReviewListView.as_view(), name='review_list'),
    path('validation_list', ScholarshipValidationListView.as_view(), name='validation_list'),
    path('review-report/<int:pk>', ScholarshipReviewReportView.as_view(), name='review_report'),
    path('select_call/', SelectCallView.as_view(), name='select_scholarship_call'),
    path('create_mastercard/<int:call_pk>', CreateMastercardScholarshipView.as_view(),
         name='add_mastercard_application'),
    path('create/<int:call_pk>', CreateScholarshipView.as_view(), name='add_application'),
    path('<int:pk>/view/', ScholarshipapplicationDetailView.as_view(), name="view_scholarship"),
    path('<int:pk>/Review/', ScholarshipapplicationReviewView.as_view(), name="review_scholarship"),
    path('<int:pk>/View/Reviewed/Application', ScholarshipapplicationRewiewDetailView.as_view(),
         name="view_scholarship_review"),
    path('<int:pk>/edit_mastercard/', UpdateMastercardScholarshipView.as_view(), name="edit_mastercard_scholarship"),
    path('<int:pk>/delete/', ScholarshipapplicationDeleteView.as_view(), name="remove_application"),
    path('<int:pk>/edit_scholarship/', UpdateScholarshipView.as_view(), name="edit_scholarship"),
    path('<int:pk>/review/add/', AddReviewView.as_view(), name="add_review"),
    path('assign_application_reviewers/', CreatScholarReviewerView.as_view(), name="assign_application_reviewers"),
    path('save-reviewers/', AssignReviewerView.as_view(), name="save_reviewers"),
    path('print/scholarship/<int:pk>', ScholarshipPrintView.as_view(), name="print_scholarship"),
    path('<int:pk>/approve/application', CreateScholarshipApprovalView.as_view(), name="approve_scholarship"),
    path('<int:pk>/reject', ScholarshipApplicationRejectView.as_view(), name="reject_scholarship_application"),
    path('application_decision', ScholarshipsApplicationDecisionListView.as_view(),
         name="scholarship_application_decision_list"),
    path('scholarship', AwardedScholarshipsListView.as_view(), name='scholarship_list'),
    path('<int:pk>/validate', ScholarshipapplicationValidationView.as_view(), name='validate_scholarship'),
    path('<int:pk>/save/validation/', ScholarshipApplicationValidateView.as_view(),
         name="validate_scholarship_application"),

   path('<int:pk>/edit/scholarship/', EditScholarshipView.as_view(), name="update_scholarship"),
    path('<int:pk>/view/scholarship/', AwardedScholarshipDetailView.as_view(), name="view_awarded_scholarship"),
]
