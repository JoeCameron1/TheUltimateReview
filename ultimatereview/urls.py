from django.conf.urls import patterns, url
from ultimatereview import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^myreviews/', views.myreviews, name='myreviews'),
                       url(r'^singlereview/(?P<review_name_slug>[\w\-]+)/$', views.single_review, name='single_review'),
                       url(r'^editreview/(?P<review_name_slug>[\w\-]+)/$', views.edit_review, name='edit_review'),
                       url(r'^singlereview/(?P<review_name_slug>[\w\-]+)/AbstractPool/$', views.AbstractPool, name='AbstractPool'),
                       url(r'^myprofile/', views.myprofile, name='myprofile'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^query/$', views.indexQueried, name='query'),
                       )
