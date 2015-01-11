from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    url(r'^submit_file$', views.submit_file, name='submit_file'),
    url(r'^submit_text$', views.submit_text, name='submit_text'),
    url(r'^$', views.index, name='index'),
)