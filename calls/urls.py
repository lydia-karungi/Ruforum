from django.urls import path, re_path, include
from calls.views import (
    CallsListView,
    ScholarshipCallsListView,
    CreateCallView,
    CallDetailView,
    CallUpdateView,
    CallDeleteView,
    CreateScholarshipCallView,ScholarshipCallUpdateView,ScholarshipCallDetailView,ScholarshipCallDeleteView
    ,load_sub_themes,FellowshipCallListView,CreateFellowshipCallView,
    FellowshipCallDetailView,FellowshipCallUpdateView,FellowshipCallDeleteView,FellowshipCallPrintView,
    GrantCallPrintView,ScholarshipCallPrintView,
    CommodityFocusDeleteView,SubthemeDeleteView,ProposalThemeDeleteView,
    #DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView
    CommodityCreatePopup,CommodityEditPopup,get_commodity_id,ThemeCreatePopup,ThemeEditPopup,get_theme_id
    ,SubThemeCreatePopup,SubThemeEditPopup,get_subtheme_id
)
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'scholarshipcalls', views.ScholarshipViewSet, basename='Call')
router.register(r'grantcalls', views.GrantCallViewSet, basename='GrantCall')
router.register(r'fellowshipcalls', views.FellowshipCallViewSet, basename='FellowshipCall')



app_name = 'calls'


urlpatterns = [
    path('api/', include(router.urls)),
    path('', CallsListView.as_view(), name='list'),
    path('scholarship-list', ScholarshipCallsListView.as_view(), name='scholarship-list'),
    path('create/', CreateCallView.as_view(), name='add_call'),
    path('scholarship/call/create/',CreateScholarshipCallView.as_view(),name='add_scholar_call'),
    path('<int:pk>/view/', CallDetailView.as_view(), name="view_call"),
    path('<int:pk>/scholarship/view/', ScholarshipCallDetailView.as_view(), name="view_scholarshipcall"),
    path('<int:pk>/edit/', CallUpdateView.as_view(), name="edit_call"),
    path('<int:pk>/Scholarshipcall/edit/', ScholarshipCallUpdateView.as_view(), name="edit_scholarshipcall"),
    path('<int:pk>/delete/', CallDeleteView.as_view(), name="remove_call"),
    path('<int:pk>/scholarship/delete/', ScholarshipCallDeleteView.as_view(), name="remove_scholarshipcall"),


    path('ajax/load-subthemes/', load_sub_themes, name='ajax_load_sub_themes'),
    # Fellowship calls
    path('fellowship/create/',CreateFellowshipCallView.as_view(),name='add_fellowship_call'),
    path('fellowship/list', FellowshipCallListView.as_view(), name='fellowship-list'),
    path('<int:pk>/fellowship/view/', FellowshipCallDetailView.as_view(), name="view_fellowshipshipcall"),
    path('<int:pk>/fellowshipcall/edit/', FellowshipCallUpdateView.as_view(), name="edit_fellowshipcall"),
    path('<int:pk>/fellowship/delete/', FellowshipCallDeleteView.as_view(), name="remove_fellowshipcall"),

   # print calls
    path('print/fellowship_call/<int:pk>', FellowshipCallPrintView.as_view(), name="print_fellowshipcall"),
    path('print/grant_call/<int:pk>', GrantCallPrintView.as_view(), name="print_grantcall"),
    path('print/scholarship_call/<int:pk>', ScholarshipCallPrintView.as_view(), name="print_scholarshipcall"),
# pop urls for commodity focus
    path('commodity_focus/create', CommodityCreatePopup, name = "commodity_focusCreate"),
    path('commodity_focus/<int:pk>/edit', CommodityEditPopup, name = "commodity_focusEdit"),
    path('commodity_focus/ajax/get_commodity_focus_id', get_commodity_id, name = "get_commodity_focus_id"),
    path('<int:pk>/commodity_focus/delete/', CommodityFocusDeleteView.as_view(), name="remove_commodity_focus"),

# pop urls for theme
    path('theme/create', ThemeCreatePopup, name = "theme_create"),
    path('theme/<int:pk>/edit', ThemeEditPopup, name = "edit_theme"),
    path('theme/ajax/get_theme_id', get_theme_id, name = "get_theme_id"),
    path('<int:pk>/theme/delete/', ProposalThemeDeleteView.as_view(), name="remove_theme"),

# pop urls for subthem
    path('subtheme/create', SubThemeCreatePopup, name = "subtheme_create"),
    path('subtheme/<int:pk>/edit', SubThemeEditPopup, name = "edit_subtheme"),
    path('subtheme/ajax/get_subtheme_id', get_subtheme_id, name = "get_subtheme_id"),
    path('<int:pk>/subtheme/delete/', SubthemeDeleteView.as_view(), name="remove_subtheme"),
]
