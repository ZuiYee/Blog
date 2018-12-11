from django.conf.urls import url
from . import views


app_name = 'spider'


urlpatterns = [
    url(r'^spider/', views.index, name='index'),
]