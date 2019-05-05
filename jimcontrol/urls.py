from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import url
from . import views;
from index.views import MarkComplain, Deletepin, ClearRequests,AdminProcessRequest, SuspendStaff, AllowStaff, StaffProcessRequest

urlpatterns = [
	url(r'^staff/$', views.staffsignin, name='staffsignin'),
	url(r'^staff/requests/$', views.staffrequests, name='staffrequests'),
	url(r'^staff/profile/$', views.staffprofile, name='staffprofile'),
	url(r'^staff/members/$', views.staffmembers, name='staffmembers'),
	url(r'^staff/complains/$', views.staffcomplains, name='staffcomplains'),
	url(r'^staff/signout/$', views.staffsignout, name='staffsignout'),

	url(r'^admin/$', views.adminsignin, name='adminsignin'),
	# url(r'^admin/process/(?P<req_id>[0-9]+)$', views.adminprocessrequest, name='adminprocessrequest'),
	url(r'^admin/createmyadmin/$', views.createadmin, name='createadmin'),
	url(r'^admin/forgetpass/$', views.forgetpass, name='forgetpass'),
	url(r'^admin/resetpincode/$', views.resetpincode, name='resetpincode'),
	url(r'^admin/requests/$', views.adminrequests, name='adminrequests'),
	url(r'^admin/pin/$', views.adminGeneratePin, name='adminGeneratePin'),
	url(r'^admin/changepin/$', views.changepin, name='changepin'),
	url(r'^admin/changepassword/$', views.changepassword, name='changepassword'),
	url(r'^admin/members/$', views.adminmembers, name='adminmembers'),
	url(r'^admin/signout/$', views.adminsignout, name='adminsignout'),
	url(r'^admin/createstaff/$', views.createstaff, name='createstaff'),
	url(r'^admin/sendmessage/$', views.sendmessage, name='sendmessage'),
	url(r'^admin/complains/$', views.admincomplains, name='admincomplains'),
	url(r'^admin/updatejob/(?P<pk>[0-9]+)/$', views.updatejob, name='updatejob'),
	url(r'^admin/deletestaff/(?P<pk>[0-9]+)/$', views.deletestaff, name='deletestaff'),

	url(r'^staff/complain/(?P<status>[A-Za-z]+)/(?P<pk>[0-9]+)/$', MarkComplain.as_view(), name='markcomplain'),
	url(r'^staff/clearrequests/(?P<level>[0-9]+)/$', ClearRequests.as_view(), name='clearrequests'),
	url(r'^staff/processrequest/(?P<pk>[0-9]+)/$', StaffProcessRequest.as_view(), name='staffprocessrequest'),
	url(r'^admin/processrequest/(?P<pk>[0-9]+)/$', AdminProcessRequest.as_view(), name='adminprocessrequest'),
	url(r'^admin/suspendstaff/(?P<pk>[0-9]+)/$', SuspendStaff.as_view(), name='suspendstaff'),
	url(r'^admin/allowstaff/(?P<pk>[0-9]+)/$', AllowStaff.as_view(), name='allowstaff'),
	url(r'^admin/deletepin/(?P<pk>[0-9]+)/$', Deletepin.as_view(), name='deletepin'),

]

urlpatterns = format_suffix_patterns(urlpatterns)