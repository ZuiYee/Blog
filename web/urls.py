from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path
app_name = 'web'


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^blogHome/', views.blogHome, name='blogHome'),
    url(r'^about/', views.about, name='about'),
    url(r'^detail/(?P<key>.*?)$', views.detail, name='detail'),

]

