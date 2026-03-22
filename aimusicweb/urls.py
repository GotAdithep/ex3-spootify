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
from django.urls import path
from user.views import create_user, read_user, update_user
from song_gen_request.views import create_song_gen_request, read_song_gen_request, update_song_gen_request
from song.views import create_song, read_song, update_song
from shared_link.views import create_shared_link, read_shared_link, update_shared_link

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-user/', create_user, name="create_user"),
    path('create-song-gen-request/', create_song_gen_request, name="create_song_gen_request"),
    path('create-song/',create_song, name="create_song"),
    path('create-shared-link',create_shared_link, name="create_shared_link"),
    path('read-user', read_user, name="read_user"),
    path('read-song-gen-request', read_song_gen_request, name="read_song_gen_request"),
    path('read-song', read_song, name="read_song"),
    path('read-shared-link', read_shared_link, name="read_shared_link"),
    path("update-user/<int:user_id>/", update_user, name="update_user"),
    path("update-song-gen-request/<int:request_id>/", update_song_gen_request, name="update_song_gen_request"),
    path("update-song/<int:song_id>/", update_song, name="update_song"),
    path("update-shared-link/<int:link_id>/", update_shared_link, name="update_shared_link"),
]
