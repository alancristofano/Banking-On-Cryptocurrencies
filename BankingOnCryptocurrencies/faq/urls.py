from django.conf.urls import include, url
from faq import views

urlpatterns=[
url(r'^$', views.questions, name='questions'),
]
