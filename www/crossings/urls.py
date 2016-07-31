from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^crossings/(?P<crossingId>[0-9]+)/comments\.json$', views.comments,
        name='comments'),
    url(r'^crossings/(?P<crossingId>[0-9]+)/comment$', views.addComment,
        name='add comment'),
    url(r'^crossings/(?P<crossingId>[0-9]+)/$', views.detail, name='detail'),
    url(r'^crossings/$', views.allCrossings, name='all'),
    url(r'^text/$', views.text, name='text'),
    url(r'^text/(?P<countryFrom>[^/]+)/(?P<countryTo>[^/]+)$',
        views.textFromTo, name='text from to'),
    url(r'^text/(?P<countryFrom>[^/]+)/(?P<countryTo>[^/]+)/(?P<name>[^/]+)$',
        views.textCrossing, name='text crossing'),
]
