from django.conf.urls import include, url
from portada import views

urlpatterns=[
url(r'^$', views.index, name='index'),

]
