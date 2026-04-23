"""
URL configuration for aimusicweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import TemplateView
from apps.user.views import SignupView, LoginView, LogoutView, CreateUserView, ListUserView, UpdateUserView, DeleteUserView
from apps.song_gen_request.views import CreateSongGenRequestView, ListSongGenRequestView, UpdateSongGenRequestView, DeleteSongGenRequest, SongGenStatusView
from apps.song.views import CreateSongView, ListSongView, UpdateSongView, DeleteSongView, LibraryView
from apps.shared_link.views import CreateShareLinkView, SharedSongView

def google_login_redirect(request):
    return redirect('/account/google/login/?process=login')

urlpatterns = [
    #in use path
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('library/', LibraryView.as_view(template_name='library.html'), name='library'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    #path('signup/', SignupView.as_view(template_name='signup.html'), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-song-form/', CreateSongGenRequestView.as_view(), name="create_song_form"),
    path('get-song-status/<str:taskId>/', SongGenStatusView.as_view(), name='get-song-status'),
    path('login/google', google_login_redirect, name="login_google"),
    path('songs/<int:song_id>/share/', CreateShareLinkView.as_view(), name="create_share_link"),
    path('s/<str:token>/', SharedSongView.as_view(), name="shared_song"),

    #unused path
    path('create-user/', CreateUserView.as_view(), name="create_user"),
    #path('create-song-gen-request/', CreateSongGenRequestView.as_view(), name="create_song_gen_request"),
    path('create-song/',CreateSongView.as_view(), name="create_song"),
    path('read-user', ListUserView.as_view(), name="read_user"),
    path('read-song-gen-request', ListSongGenRequestView.as_view(), name="read_song_gen_request"),
    path('read-song', ListSongView.as_view(), name="read_song"),
    path("update-user/<int:user_id>/", UpdateUserView.as_view(), name="update_user"),
    path("update-song-gen-request/<int:request_id>/", UpdateSongGenRequestView.as_view(), name="update_song_gen_request"),
    path("update-song/<int:song_id>/", UpdateSongView.as_view(), name="update_song"),
    path("delete-user/<int:user_id>/", DeleteUserView.as_view(), name="delete_user"),
    path("delete-song-gen-request/<int:request_id>/", DeleteSongGenRequest.as_view(), name="delete_song_gen_request"),
    path("delete-song/<int:song_id>/", DeleteSongView.as_view(), name="delete_song"),
]
