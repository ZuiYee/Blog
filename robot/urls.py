from django.conf.urls import url
from . import views


app_name = 'robot'


urlpatterns = [
    url(r'^myrobot/', views.myrobot, name='myrobot'),
]