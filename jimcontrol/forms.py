from django import forms
from .models import AdminUser, Staff, Agent


class AdminUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = AdminUser
		fields = ['firstname', 'lastname', 'username','password', 'email']


class StaffUserForm(forms.ModelForm):

	class Meta:
		model = Staff
		fields = ['firstname', 'lastname', 'username','password', 'job']


class AgentUserForm(forms.ModelForm):

	class Meta:
		model = Agent
		fields = ['username','password', 'phoneno']
