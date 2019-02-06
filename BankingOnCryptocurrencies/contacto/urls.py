from django.conf.urls import include, url
from contacto import views

urlpatterns=[
url(r'^$', views.contact , name='contact'),
]
