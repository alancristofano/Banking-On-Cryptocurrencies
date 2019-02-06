from django.conf.urls import include, url
from registro import views

urlpatterns=[
url(r'^signin/', views.signin, name='signin'),
url(r'^register/', views.registro, name='register'),
url(r'^signout/', views.signout, name='singout'),

]

