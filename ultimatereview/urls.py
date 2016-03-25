from django.conf.urls import patterns, url
from ultimatereview import views

urlpatterns = patterns('',
                        url(r'^$', views.index, name='index'),
                        url(r'^register/$', views.register, name='register'),
                        url(r'^login/$', views.user_login, name='login'),
                        url(r'^about/$', views.about, name='about'),
                        url(r'^myreviews/', views.myreviews, name='myreviews'),
                        url(r'^editreview/(?P<review_name_slug>[\w\-]+)/$', views.edit_review, name='edit_review'),
                        url(r'^singlereview/(?P<review_name_slug>[\w\-]+)/$', views.single_review, name='single_review'),
                        url(r'^singlereview/(?P<review_name_slug>[\w\-]+)/AbstractPool/$', views.AbstractPool, name='AbstractPool'),
                        url(r'^singlereview/(?P<review_name_slug>[\w\-]+)/DocumentPool/$', views.document_pool, name='DocumentPool'),
						url(r'^singlereview/(?P<review_name_slug>[\w\-]+)/FinalPool/$', views.final_pool, name='FinalPool'),
                        url(r'^myprofile/', views.myprofile, name='myprofile'),
                        url(r'^logout/$', views.user_logout, name='logout'),
                        url(r'^query/$', views.indexQueried, name='query'),
						url(r'^query_results/', views.query_results, name='query_results'),
                        )
