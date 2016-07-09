from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^crossings/(?P<crossingId>[0-9]+)/comments\.json$', views.comments,
        name='comments'),
    url(r'^crossings/(?P<crossingId>[0-9]+)/comment$', views.addComment,
        name='add comment'),
    url(r'^crossings/(?P<crossingId>[0-9]+)/$', views.detail, name='detail'),
]
