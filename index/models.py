from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
	phoneno = models.CharField(max_length=20)
	pincode = models.CharField(max_length=250)
	bankname = models.CharField(max_length=250)
	accname = models.CharField(max_length=1000)
	sponsor = models.CharField(max_length=1000, default='Jimmoney')
	accno = models.CharField(max_length=20)
	regcode = models.CharField(max_length=20)
	network = models.IntegerField(default=0)
	totearning = models.IntegerField(default=0)
	balance = models.IntegerField(default=0)
	accstatus = models.CharField(max_length=250, default='active')
	level = models.IntegerField(default=0)
	dateofmembership = models.DateTimeField(auto_now=True)
	# dateofmembership = models.DateTimeField(default=datetime.datetime.now())

	def __str__(self):
		return self.username

class Sponsorship(models.Model):
	sponsor = models.ForeignKey(User, default=1) # object of the sponsor
	member = models.CharField(max_length=500) # username of the brought in member
	

# Real request to display all request from day 1
class Request(models.Model):
	user = models.ForeignKey(User, default=1)
	bankname = models.CharField(max_length=250, default='Jim')
	accname = models.CharField(max_length=1000, default='Jim')
	accno = models.CharField(max_length=20, default='0')
	amount = models.CharField(max_length=20)
	level = models.CharField(max_length=10, default=2); # level the money was requested
	staffstatus = models.BooleanField(default=False)
	adminstatus = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now=True)

class Newrequest(models.Model):
	request = models.ForeignKey(Request)
	level = models.CharField(max_length=10, default=2)