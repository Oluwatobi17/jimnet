from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from . import views;

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^signup/$', views.register, name='register'),
	url(r'^api/usernames/$', views.Usernames.as_view(), name='usernames'),
	url(r'^signout/$', views.logout, name='logout'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^withdraw/$', views.withdraw, name='withdraw'),
	url(r'^editprofile/$', views.editprofile, name='editprofile'),
	url(r'^paymenthistory/$', views.paymenthistory, name='paymenthistory'),
	url(r'^forgetpass/$', views.forgetpass, name='forgetpass'),
	url(r'^complain/$', views.complain, name='complain'),
	url(r'^forgetpincode/$', views.forgetpincode, name='forgetpincode'),
	
]


urlpatterns = format_suffix_patterns(urlpatterns)