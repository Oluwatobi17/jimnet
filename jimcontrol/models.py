from django.db import models
import django
# Basically Admin'models

class AdminUser(models.Model):
	email = models.EmailField(max_length=500, default='jhawwal@yahoo.com')
	username = models.CharField(max_length=250)
	firstname = models.CharField(max_length=250)
	lastname = models.CharField(max_length=250)
	password = models.CharField(max_length=1000)
	pincode = models.CharField(max_length=250, default='cjmsgf478') # ladipo753
	note = models.IntegerField(default=0)

	def __str__(self):
		return self.username

class AdminNotification(models.Model):
	message = models.CharField(max_length=5000)
	date = models.DateTimeField(default=django.utils.timezone.now())


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

class Agent(models.Model):
	username = models.CharField(max_length=250)
	password = models.CharField(max_length=1000)
	lastlogin = models.DateTimeField(auto_now=django.utils.timezone.now())
	phoneno = models.CharField(max_length=20)
	balance = models.IntegerField(default=0)

	def __str__(self):
		return self.username