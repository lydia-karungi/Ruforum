from django.urls import path
from fellowship.views import (
    FellowshipsListView,
    CreateFellowshipView,
    FellowshipUpdateView,
    FellowshipReviewView,
    FellowshipCommentsView,CreateFellowshipTypeView,FellowshipTypeListView,FellowshipTypeUpdateView,
    FellowshipTypeDetailView,FellowshipTypeDeleteView,FellowshipTypeDeleteView
    # RemoveContactView,
    #GetContactsView, AddCommentView, UpdateCommentView,
    #DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView
)

from django.views.decorators.http import require_POST

app_name = 'fellowship'


urlpatterns = [
    path('', FellowshipsListView.as_view(), name='list'),
    path('create/', CreateFellowshipView.as_view(), name='add_fellowship'),
    path('<int:pk>/edit/', FellowshipUpdateView.as_view(), name="edit_fellowship"),
    path('<int:pk>/review/', FellowshipReviewView.as_view(), name="review_fellowship"),
    path('<int:pk>/comments/', require_POST(FellowshipCommentsView.as_view()), name="save_fellowship_comments"),
    
    #path('<int:pk>/delete/',
    #     RemoveContactView.as_view(),
    #     name="remove_contact"),

    #path('get/list/', GetContactsView.as_view(), name="get_contacts"),

    #path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    #path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    #path('comment/remove/',
    #     DeleteCommentView.as_view(),
    #     name="remove_comment"),

    #path('attachment/add/',
    #     AddAttachmentsView.as_view(),
    #     name="add_attachment"),
    #path('attachment/remove/', DeleteAttachmentsView.as_view(),
    #     name="remove_attachment"),


    # Fellowship type urls
    path('fellowship_type/create/',CreateFellowshipTypeView.as_view(),name='add_fellowship_type'),
    path('fellowship_type/list', FellowshipTypeListView.as_view(), name='fellowship_type_list'),
    path('<int:pk>/fellowship_type/view/', FellowshipTypeDetailView.as_view(), name="view_fellowshipship_type"),
    path('<int:pk>/fellowship_type/edit/', FellowshipTypeUpdateView.as_view(), name="edit_fellowship_type"),
    path('<int:pk>/fellowship_type/delete/', FellowshipTypeDeleteView.as_view(), name="remove_fellowship_type"),

]
