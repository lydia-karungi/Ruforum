from django.urls import path
from grant_types.views import (
    GranttypesListView,
    CreateGranttypeView,GrantTypeUpdateView,
    GrantTypeDetailView,GrantTypeDeleteView
    #UpdateContactView, RemoveContactView,
    #GetContactsView, AddCommentView, UpdateCommentView,
    #DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView
)

app_name = 'grant_types'


urlpatterns = [
    path('', GranttypesListView.as_view(), name='list'),
    path('create/', CreateGranttypeView.as_view(), name='add_grant_type'),
    path('<int:pk>/view/', GrantTypeDetailView.as_view(), name="view_grant_type"),
    path('<int:pk>/edit/', GrantTypeUpdateView.as_view(), name="edit_grant_type"),
    path('<int:pk>/delete/',GrantTypeDeleteView.as_view(),name="remove_grantType"),

]
