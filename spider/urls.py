from django.conf.urls import url
from . import views


app_name = 'spider'


urlpatterns = [
    url(r'^mainspider/', views.mainspider, name='mainspider'),
    url(r'^EducationSpider/', views.EducationSpider, name='EducationSpider'),
    url(r'^TestSpider/', views.TestSpider, name='TestSpider'),
]