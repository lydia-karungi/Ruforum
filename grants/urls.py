from django.urls import path
from grants.views import (
    GrantsListView,
    CreateGrantView,
    GrantsReportView,
    GrantUpdateView,
    GrantReviewView,
    GrantCommentsView,
    Month6View,
    CreateGrantApprovalView, Month12View, Month18View, Month24View, Month30View, LastReportView, Month36View,
    Month42View, Month48View, Month54View, Month60View, Month66View, Month72View, Month78View, Month84View, Month90View,
    Month96View, Month102View, Month108View,
    GrantDeleteView,
    # GetContactsView, AddCommentView, UpdateCommentView,
    # DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView
)

from django.views.decorators.http import require_POST

app_name = 'grants'


urlpatterns = [
    path('', GrantsListView.as_view(), name='list'),
    path('reports/', GrantsReportView.as_view(), name='grants_reports'),
    path('create/', CreateGrantView.as_view(), name='add_grant'),
    path('<int:pk>/edit/', GrantUpdateView.as_view(), name="edit_grant"),
    path('<int:pk>/review/', GrantReviewView.as_view(), name="review_grant"),
    path('<int:pk>/delete/', GrantDeleteView.as_view(), name="remove_grant"),
    path('<int:pk>/comments/', require_POST(GrantCommentsView.as_view()), name="save_grant_comments"),
    path('<int:pk>/month6/', Month6View.as_view(), name="view_month6"),
    path('<int:pk>/month12/', Month12View.as_view(), name="view_month12"),
    path('<int:pk>/month18/', Month18View.as_view(), name="view_month18"),
    path('<int:pk>/month24/', Month24View.as_view(), name="view_month24"),
    path('<int:pk>/month30/', Month30View.as_view(), name="view_month30"),
    path('<int:pk>/month36/', Month36View.as_view(), name="view_month36"),
    path('<int:pk>/month42/', Month42View.as_view(), name="view_month42"),
    path('<int:pk>/month48/', Month48View.as_view(), name="view_month48"),
    path('<int:pk>/month54/', Month54View.as_view(), name="view_month54"),
    path('<int:pk>/month60/', Month60View.as_view(), name="view_month60"),
    path('<int:pk>/month66/', Month66View.as_view(), name="view_month66"),
    path('<int:pk>/month72/', Month72View.as_view(), name="view_month72"),
    path('<int:pk>/month78/', Month78View.as_view(), name="view_month78"),
    path('<int:pk>/month84/', Month84View.as_view(), name="view_month84"),
    path('<int:pk>/month90/', Month90View.as_view(), name="view_month90"),
    path('<int:pk>/month96/', Month96View.as_view(), name="view_month96"),
    path('<int:pk>/month102/', Month102View.as_view(), name="view_month102"),
    path('<int:pk>/month108/', Month108View.as_view(), name="view_month108"),

    #path('<int:pk>/delete/',
    #     RemoveContactView.as_view(),
    #     name="remove_contact"),
    path('<int:pk>/last/report', LastReportView.as_view(), name="view_last_report"),
    path('<int:pk>/approve/', CreateGrantApprovalView.as_view(), name="approve_grant"),
]
