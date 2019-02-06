from django.conf.urls import include, url
from consulta import views

urlpatterns=[
url(r'^$', views.search, name='search'),
url(r'^(?P<coin_id>.*)/$', views.coin_selected, name='coin_selected'),
url(r'^(?P<coin_id>.*)/result', views.result, name='result'),

]
