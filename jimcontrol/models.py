from django.db import models
# Basically Admin'models

class AdminUser(models.Model):
	email = models.EmailField(max_length=500, default='jimnet@gmail.com')
	username = models.CharField(max_length=250)
	firstname = models.CharField(max_length=250)
	lastname = models.CharField(max_length=250)
	password = models.CharField(max_length=1000)
	pincode = models.CharField(max_length=250, default='cjmsgf478') # ladipo753

	def __str__(self):
		return self.username


class Staff(models.Model):
	username = models.CharField(max_length=250)
	firstname = models.CharField(max_length=250)
	lastname = models.CharField(max_length=250)
	password = models.CharField(max_length=1000)
	job = models.CharField(max_length=10)
	status = models.CharField(max_length=10, default='active')
	lastlogin = models.DateTimeField()

	def __str__(self):
		return self.username

class Registrationcode(models.Model):
	code = models.CharField(max_length=10)
	status = models.BooleanField(default=False) # True means it has been used
	date = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.code