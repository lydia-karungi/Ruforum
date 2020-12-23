from django.urls import path, include
from hrm.views import (
    DepartmentsListView,
    CreateDepartmentView,
    DepartmentDetailView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    StaffProfilesListView,
    CreateStaffProfileView,
    StaffProfileDetailView,
    StaffProfileUpdateView,
    StaffProfileDeleteView,
    StaffTravelsListView,
    CreateStaffTravelView,
    StaffTravelDetailView,
    StaffTravelUpdateView,
    StaffTravelDeleteView,
    AssetCategorysListView,
    CreateAssetCategoryView,
    AssetCategoryDetailView,
    AssetCategoryUpdateView,
    AssetCategoryDeleteView,
    AssetsListView,
    CreateAssetView,
    AssetDetailView,
    AssetUpdateView,
    AssetDeleteView,
    LeavesListView,
    CreateLeaveView,
    LeaveUpdateView,
    LeaveDeleteView,
    VehiclesListView,Month6AppraisalListView,CreateMonth6AppraisalView,
    CreateVehicleView,ApproveLeaveApplicationView,ApprovedLeavesListView,
    VehicleDetailView,LeaveApplicationHRCommentView,LeaveSupervisorRecommendationView,
    VehicleUpdateView,EditLeaveAssignmentView,EditLeaveApplicationView,
    VehicleDeleteView,CreateLeaveAssignmentView,CreateLeaveApplicationView,LeavesApplicationListView,
    CalendarView, AssignAssetView, ContractListView, CreateContractView, ContractUpdateView, ContractDetailView,
    ContractDeleteView, AddAttachmentView,LeavesAssignmentListView
)
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'leave_types', views.LeaveViewSet)
router.register(r'assignment', views.LeaveAssignmentViewSet)
router.register(r'leave_applications', views.LeaveApplicationViewSet, basename='leave_application')
router.register(r'leaves', views.ApprovedLeaveViewSet, basename='leave')
router.register(r'month6appraisals', views.AppraisalViewSet, basename='month6_appraisal')
app_name = 'hrm'


urlpatterns = [
    path('api/', include(router.urls)),
    path('departments/', DepartmentsListView.as_view(), name='department_list'),
    path('create_dept/', CreateDepartmentView.as_view(), name='add_department'),
    path('<int:pk>/view_dept/', DepartmentDetailView.as_view(), name="view_department"),
    path('<int:pk>/edit_dept/', DepartmentUpdateView.as_view(), name="edit_department"),
    path('<int:pk>/delete_dept/',
         DepartmentDeleteView.as_view(),
         name="remove_department"),

    path('staff/', StaffProfilesListView.as_view(), name='staff_list'),
    path('create_staff/', CreateStaffProfileView.as_view(), name='add_staff'),
    path('<int:pk>/view_staff/', StaffProfileDetailView.as_view(), name="view_staff"),
    path('<int:pk>/edit_staff/', StaffProfileUpdateView.as_view(), name="edit_staff"),
    path('<int:pk>/delete_staff/',
         StaffProfileDeleteView.as_view(),
         name="remove_staff"),

    path('travel/', StaffTravelsListView.as_view(), name='travel_list'),
    path('create_travel/', CreateStaffTravelView.as_view(), name='add_travel'),
    path('<int:pk>/view_travel/', StaffTravelDetailView.as_view(), name="view_travel"),
    path('<int:pk>/edit_travel/', StaffTravelUpdateView.as_view(), name="edit_travel"),
    path('<int:pk>/delete_travel/',
         StaffTravelDeleteView.as_view(),
         name="remove_travel"),

    path('asset_categories/', AssetCategorysListView.as_view(), name='asset_category_list'),
    path('create_asset_category/', CreateAssetCategoryView.as_view(), name='add_asset_category'),
    path('<int:pk>/view_asset_category/', AssetCategoryDetailView.as_view(), name="view_asset_category"),
    path('<int:pk>/edit_asset_category/', AssetCategoryUpdateView.as_view(), name="edit_asset_category"),
    path('<int:pk>/delete_asset_category/',
         AssetCategoryDeleteView.as_view(),
         name="remove_asset_category"),

    path('assets/', AssetsListView.as_view(), name='asset_list'),
    path('create_asset/', CreateAssetView.as_view(), name='add_asset'),
    path('<int:pk>/view_asset/', AssetDetailView.as_view(), name="view_asset"),
    path('<int:pk>/edit_asset/', AssetUpdateView.as_view(), name="edit_asset"),
    path('<int:pk>/assign_asset/', AssignAssetView.as_view(), name="assign_asset"),
    path('<int:pk>/delete_asset/',
         AssetDeleteView.as_view(),
         name="remove_asset"),

    path('leavestypes/', LeavesListView.as_view(), name='leave_list'),
    path('leave/assignments',LeavesAssignmentListView.as_view(), name='leave_assignments'),
    path('leave/assigment', CreateLeaveAssignmentView.as_view(),name='add_leave_assignment' ),
    path('create_leave/', CreateLeaveView.as_view(), name='add_leave'),
    path('<int:pk>/edit_leave/', LeaveUpdateView.as_view(), name="edit_leave"),
    path('<int:pk>/delete_leave/',
         LeaveDeleteView.as_view(),
         name="remove_leave"),
    path('vehicles/', VehiclesListView.as_view(), name='vehicle_list'),
    path('create_vehicle/', CreateVehicleView.as_view(), name='add_vehicle'),
    path('<int:pk>/view_vehicle/', VehicleDetailView.as_view(), name="view_vehicle"),
    path('<int:pk>/edit_vehicle/', VehicleUpdateView.as_view(), name="edit_vehicle"),
    path('<int:pk>/delete_vehicle/',
         VehicleDeleteView.as_view(),
         name="remove_vehicle"),

    path('calendar/', CalendarView.as_view(), name='calendar'),
    # contract  details
    path('contracts/', ContractListView.as_view(), name='contract_list'),
    path('create_contract/', CreateContractView.as_view(), name='add_contract'),
    path('<int:pk>/view_contract/', ContractDetailView.as_view(), name="view_contract"),
    path('<int:pk>/edit_contract/', ContractUpdateView.as_view(), name="edit_contract"),
    path('<int:pk>/delete_contract/',ContractDeleteView.as_view(),name="remove_contract"),
    path('attachment/add/', AddAttachmentView.as_view(), name="add_travel_attachment"),
    path('leaveapplications/',LeavesApplicationListView.as_view(),name='leave_applications'),
    path('approved/leaves/',ApprovedLeavesListView.as_view(),name='approved_leaves'),
    path('leave/application/', CreateLeaveApplicationView.as_view(), name='add_leave_application'),
    path('<int:pk>/edit/leave/application/', EditLeaveApplicationView.as_view(), name="edit_leave_application"),
    path('<int:pk>/leave/comment/', LeaveApplicationHRCommentView.as_view(), name="leave_application_hr_comment"),
    path('<int:pk>/edit/leave/assignment/', EditLeaveAssignmentView.as_view(), name="edit_leave_assigment"),
    path('<int:pk>/leave/recommendation', LeaveSupervisorRecommendationView.as_view(), name="leave_application_sp_rcm"),
    path('<int:pk>/leave/application/details/',ApproveLeaveApplicationView.as_view(), name='approve_leave_application'),

    # Appraisals
    path('month6/appraisals/',Month6AppraisalListView.as_view(),name='month6_appraisals'),
    path('create/month6/appraisal', CreateMonth6AppraisalView.as_view(), name='add_month6_appraisal'),

]
