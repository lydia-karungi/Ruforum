from django.contrib.auth import views as auth_views

from django.urls import path
from common.views import (
    HomeView, LoginView, ForgotPasswordView, LogoutView,
    ChangePasswordView, ProfileView, UpdateProfileView,
    UsersListView, CreateUserView, UpdateUserView, UserDetailView,
    UserDeleteView, PasswordResetView,
    change_password_by_admin, change_user_status,
    GroupsListView, CreateGroupView,
    UpdateGroupView, GroupDetailView, GroupDeleteView,
    signup,
    account_activation_sent,
    activate,
    DocumentListView, document_create, document_update,
    DocumentDetailView, DocumentDeleteView,
    download_document, change_user_status, download_attachment,getUserData,getCallsData
)
from django.conf.urls.static import static
from django.conf import settings


app_name = 'common'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/users',getUserData , name='user_api'),
    path('api/calls',getCallsData,name="calls_api"),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/',
         ForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/',
         ChangePasswordView.as_view(), name='change_password'),
    path('users/<int:pk>/update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # User views
    path('users/list/', UsersListView.as_view(), name='users_list'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/edit/', UpdateUserView.as_view(), name="edit_user"),
    path('users/<int:pk>/view/', UserDetailView.as_view(), name='view_user'),
    path('users/<int:pk>/delete/',
         UserDeleteView.as_view(), name='remove_user'),

    path(
        'password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('change-password-by-admin/', change_password_by_admin,
         name="change_password_by_admin"),

    path('user/status/<int:pk>/',
         change_user_status, name='change_user_status'),

    path('groups/list/', GroupsListView.as_view(), name='groups_list'),
    path('groups/create/', CreateGroupView.as_view(), name='create_group'),
    path('groups/<int:pk>/edit/', UpdateGroupView.as_view(), name="edit_group"),
    path('groups/<int:pk>/view/', GroupDetailView.as_view(), name='view_group'),
    path('groups/<int:pk>/delete/',
         GroupDeleteView.as_view(), name='remove_group'),

    path('signup/', signup, name='signup'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # Document
    path('documents/', DocumentListView.as_view(), name='doc_list'),
    path('documents/create/', document_create, name='create_doc'),
    path('documents/<int:pk>/edit/', document_update, name="edit_doc"),
    path('documents/<int:pk>/view/',
         DocumentDetailView.as_view(), name='view_doc'),
    path('documents/<int:pk>/delete/',
         DocumentDeleteView.as_view(), name='remove_doc'),

    # download
    path('documents/<int:pk>/download/',
         download_document, name='download_document'),

    # download_attachment
    path('attachments/<int:pk>/download/',
         download_attachment, name='download_attachment'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
