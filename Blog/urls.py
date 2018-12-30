from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from web.views import profile
from spider.views import mainspider
from robot.views import myrobot
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', profile, name='index'),
    url(r'^profile/', profile, name='profile'),
    url(r'^mainspider/', mainspider, name='mainspider'),
    url(r'^myrobot/', myrobot, name='myrobot'),
    url(r'^web/', include('web.urls')),
    url(r'^spider/', include('spider.urls')),
    url(r'^robot/', include('robot.urls')),
    url(r"^media/(?P<path>.*)$", serve,  {"document_root": settings.MEDIA_ROOT, }),
]

