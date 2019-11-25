from django.contrib import admin
from django.urls import path
from core.views import PersonAPI, FaceAPI
from access_control.views import AccessRecordAPI, AccessRecordListAPI
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^person/?$', PersonAPI.as_view(), name="person_api"),
    url(r'^face/?$', FaceAPI.as_view(), name="face_api"),
    url(r'^record/?$', AccessRecordAPI.as_view(), name="record_api"),
    url(r'^record_list/?$', AccessRecordListAPI.as_view(), name="record_list_api"),
]
