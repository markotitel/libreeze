from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
                       url(r'^submit_file$', views.submit_file, name='submit_file'),
                       url(r'^submit_text$', views.submit_text, name='submit_text'),
                       url(r'^submit_email$', views.submit_email, name='submit_email'),
                       url(r'^verify_email$', views.verify_email, name='verify_email'),
                       url(r'^unsubscribe_project', views.unsubscribe_project, name='unsubscribe_project'),
                       url(r'^unsubscribe', views.unsubscribe, name='unsubscribe'),
                       url(r'^support', views.support, name='support'),
                       url(r'^faq', views.faq, name='faq'),
                       url(r'^$', views.index, name='index'),

#					   GUI testing purpose routes,
                       url(r'^devtest_verify_email$', views.devtest_verify_email, name='devtest_verify_email'),
                       url(r'^devtest_unsubscribe$', views.devtest_unsubscribe, name='devtest_unsubscribe'),
                       url(r'^devtest_unsubscribe_project$', views.devtest_unsubscribe_project, name='devtest_unsubscribe_project')
)
