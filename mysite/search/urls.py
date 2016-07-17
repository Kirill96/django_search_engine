from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^indexURL.html/?$', views.indexURL),
    url(r'^knownURL.html/?$', views.knownURL),
    url(r'^stateAndEdit.html/?$', views.stateAndEdit),
    url(r'^home.html/?$', views.home),
]