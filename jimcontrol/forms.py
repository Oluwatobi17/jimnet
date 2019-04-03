from django import forms
from .models import AdminUser, Staff


class AdminUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = AdminUser
		fields = ['firstname', 'lastname', 'username','password']


class StaffUserForm(forms.ModelForm):

	class Meta:
		model = Staff
		fields = ['firstname', 'lastname', 'username','password', 'job']
