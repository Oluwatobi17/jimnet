from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from .models import User, Sponsorship, Request, Newrequest
import datetime
from jimcontrol.models import Staff, Registrationcode
import random

from django.core.mail import send_mail

# Rest-api framework modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProcessingRequestSerializer
from rest_framework.permissions import IsAuthenticated



# Create your views here.
def index(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_active:

				login_user(request, user)
				user = User.objects.filter(username=request.user.username)
				
				return redirect(dashboard)
				
			else:
				messages.error(request, 'Your account has been disabled')
				return redirect(index)
		else:
			messages.error(request, 'Invalid Login')
			return redirect(index)

	# if the request is not a post
	else:
		return render(request, 'index/login.html', {
			'title': 'Jim Money Networking Business'
		})
def logout(request):
	logout_user(request)
	return redirect(index)

def dateback(referral):
	if referral =='Jimmoney':
		sponsorObj = User.objects.get(username='Jimmoney')
		sponsorObj.network += 1;
		sponsorObj.balance += 10;
		sponsorObj.totearning += 10;
		sponsorObj.level = leveldeterminant(sponsorObj.username)
		sponsorObj.save()

		return;
	else:
		# Trying to pay the sponsor of the referal=referal
		nextsponsorObj = Sponsorship.objects.get(member=referral)

		sponsorObj = User.objects.get(username=nextsponsorObj.sponsor.username)
		sponsorObj.network += 1;
		sponsorObj.balance += 10;
		sponsorObj.totearning += 10;
		sponsorObj.level = leveldeterminant(nextsponsorObj.sponsor.username)
		sponsorObj.save()

		if nextsponsorObj.sponsor.username != 'Jimmoney':
			print('running dateback')
			dateback(nextsponsorObj.sponsor.username)
		else:
			return;

	# newsponsorobj = User.objects.get(username=referral)
	# newsponsorobj.network += 1;
	# newsponsorobj.balance += 10;
	# newsponsorobj.totearning += 10;
	# newsponsorobj.level = leveldeterminant(referral)
	# newsponsorobj.save()

	# if newsponsorobj.sponsor.username != 'Jimmoney':
		
	# return True;

def leveldeterminant(username):
	user = User.objects.get(username=username)
	level = 0
	cal = False
	if len(Sponsorship.objects.filter(sponsor=user))==10:
		level = 1;

		# Looping through the list of user's sponsorship
		for member in Sponsorship.objects.filter(sponsor=user):
			mem_obj = User.objects.get(username=member.member)
			if len(Sponsorship.objects.filter(sponsor=mem_obj)) == 10:
				cal = True
			else:
				return level
		if cal:
			level = 2
			if user.network >= 1000 and user.network < 10000:
				return 3
			elif user.network >= 10000 and user.network<100000:
				return 4
			elif user.network >=100000 and user.network<10000000:
				return 5
			elif user.network >= 10000000:
				return 6;


	return level;


def treeboy(user_obj):

	li = Sponsorship.objects.filter(sponsor=user_obj) # list of user_obj sponsorship
	if li:
		for s in li:
			spon = s.sponsor.username
			member = s.member
			tree.append([ member, spon]) # set sponsor and the person sponsored
			if Sponsorship.objects.filter(sponsor=User.objects.get(username=s.member)):
				treeboy(User.objects.get(username=s.member))

	return tree;


def checksmallsponsorship(user_obj):
	referreds = Sponsorship.objects.filter(sponsor=user_obj)
	for referred in referreds:
		referred_obj = User.objects.get(username=referred.member)
		if len(Sponsorship.objects.filter(sponsor=referred_obj)) < 10:
			return referred.member; # returning the person'username as the referal

	# Choosing the nextofkin by random for sponsorship
	nextOfkin = random.choice(referreds).member

	checksmallsponsorship(nextOfkin)




def register(request):
	if request.method=='POST':
		form = UserForm(request.POST)
		if User.objects.filter(username=request.POST['username']):
			messages.error(request, 'Username is taken')
			return redirect(register)
		else:
			if form.is_valid():
				referral = request.POST['sponsor']
				if referral!='Jimmoney':
					if not User.objects.filter(username=referral): #check if the referer exist
						messages.error(request, "Sponsor Doesn't exist")
						return redirect(register)

				# Check if password 1 match password 2
				if not request.POST['password']==request.POST['password2']:
					messages.error(request, "Password 1 does not match password 2")
					return redirect(register)

				if not request.POST['pincode']==request.POST['pincode2']:
					messages.error(request, "Pincode 1 does not match pincode 2")
					return redirect(register)

				# Checking the registration code
				regcode = request.POST['regcode'].upper()
				if Registrationcode.objects.filter(code=regcode):
					code = Registrationcode.objects.get(code=regcode)
					if code.status:
						messages.error(request, 'Registration code has been used')
						return redirect(register)
				else:
					messages.error(request, 'Invalid registration code')
					return redirect(register)

				user = form.save(commit=False)
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user.set_password(password)
				user.regcode = regcode
				# user.dateofmembership = datetime.datetime.now()
				user.save()
				reg = Registrationcode.objects.get(code=regcode)
				reg.status = True;
				reg.save()

				user = authenticate(request, username=username, password=password)
				if user is not None:
					login_user(request, user)

					if username != 'Jimmoney':
						# Checking if the sponsor's L1 is complete

						sponsorObj = User.objects.get(username=referral)
						if len(Sponsorship.objects.filter(sponsor=sponsorObj)) < 10:
							user.sponsor = sponsorObj.username
							user.save()

							sponsorObj.network += 1;
							sponsorObj.balance += 20;
							sponsorObj.totearning += 20;
							sponsorObj.level = leveldeterminant(referral)
							sponsorObj.save()

							# Creating new sponsorship
							newSponsorship = Sponsorship(sponsor=sponsorObj, member=username)
							newSponsorship.save()

							# Updating the sponsor's level
							sponsor = User.objects.get(username=referral)
							sponsor.level = leveldeterminant(username)
							sponsor.save()

							if sponsorObj.username != 'Jimmoney':
								dateback(referral)

							messages.success(request, 'Registration successful. Welcome '+username)
							return redirect(dashboard)
						else:
							# print('Level full')
							# print(len(Sponsorship.objects.filter(sponsor=sponsorObj)))
							# Change sponsor to the new checksmallsponsorship() returned value


							# Getting the down side of the sponsor
							nextsponsor = checksmallsponsorship( User.objects.get(username=referral) )
							# print(nextsponsor)
							user.sponsor = nextsponsor
							user.save()
							sponsorObj = User.objects.get(username=nextsponsor)
							sponsorObj.network += 1;
							sponsorObj.balance += 20;
							sponsorObj.totearning += 20;
							sponsorObj.level = leveldeterminant(nextsponsor)
							sponsorObj.save()

							# Creating new sponsorship
							newSponsorship = Sponsorship(sponsor=sponsorObj, member=username)
							newSponsorship.save()

							dateback(referral)
							messages.success(request, 'Registration successful. Welcome '+username)
							return redirect(dashboard)

					messages.success(request, 'Registration successful. Welcome '+username)
					return redirect(dashboard)

		messages.success(request, 'Please ensure to fill all field')
		return redirect(register)
	else:
		return render(request, 'index/register.html', {
			'title': 'Sign Up today to Jim Money Networking Business'
		})

tree = [] # the tree name holder
def dashboard(request):
	if request.user.is_authenticated():
		user = User.objects.get(username=request.user.username)

		mytree = treeboy(user)
		global tree
		tree = []
		return render(request, 'index/home.html', {
			'title': 'Dashboard: Welcome to Jim money',
			'user': user,
			'treeboy': mytree
		})
	else:
		return redirect(index)


def forgetpass(request):
	username = request.POST['username']
	if username:
		user_obj = User.objects.filter(username=username)
		if user_obj:
			user = User.objects.get(username=username)
			newpassword = str(random.randint(10000, 999999))
			user.set_password(newpassword)
			emailto = user.email

			message = username+', your new password is '+newpassword

			res = send_mail("Jim password recovery", message, "ganiuibrahim3000@gmail.com",[emailto])
			print(res)
			print('Result')
			messages.success(request, 'A mail has been sent to your email')
			return redirect(index)
		else:
			messages.error(request, 'Username does not exist')
			return redirect(index)
	else:
		messages.error(request, 'Please fill the required field')
		return redirect(index)


def profile(request):
	if request.user.is_authenticated():
		return render(request, 'index/profile.html', {
			'title': 'Profile: Welcome to Jim money',
			'user': User.objects.get(username=request.user.username)
		})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(index)

def paymenthistory(request):
	if request.user.is_authenticated():
		return render(request, 'index/paymenthistory.html', {
			'title': 'Payment History: Welcome to Jim money',
			'user': User.objects.get(username=request.user.username),
			'history': Request.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date') 
		})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(index)

# Withdraw all function
# def withdrawall(request):
# 	if request.method == 'POST':
# 		if request.user.is_authenticated():
# 			user = User.objects.get(username=request.user.username)

# 			if user.balance > 999:
# 				if user.bankname and user.accno and user.accno:
# 					bal = user.balance
# 					user.balance = 0;
# 					user.save();

# 					newrequest = Request(user=user, amount=bal)
# 					newrequest.save();


# 					messages.success(request, 'Request has been placed')
# 					return redirect(dashboard)
# 				else:
# 					messages.error(request, 'Please edit your bank account details on your profile page')
# 					return redirect(dashboard)
# 			else:
# 				messages.error(request, 'Amount must be up to #1,000')
# 				return redirect(dashboard)
# 		else:
# 			messages.error(request, 'Please Sign in')
# 			return redirect(index)
# 	else:
# 		return redirect(index)

def withdraw(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			user = User.objects.get(username=request.user.username)

			if user.bankname and user.accno and user.accno:

				# Checking pincode before proceeding
				if request.POST['pincode'] == user.pincode:

					# converting the amount to integer
					requestamount = int(request.POST['amount'])

					# Ensuring the requested amount is not more than the balance
					if requestamount > user.balance:
						messages.error(request, 'Insufficient fund. You have #',user.balance)
						return redirect(dashboard)
					else:
						# Ensuring the minimum amount is 1000
						if requestamount < 10:
							messages.error(request, 'Amount must be up to #1,000')
							return redirect(dashboard)

						# Proceeding is the amount is up to #1,000
						bal = user.balance
						user.balance -= requestamount;
						user.save();

						newrequest = Request()
						newrequest.user = user
						newrequest.amount = requestamount
						newrequest.bankname = user.bankname
						newrequest.accname = user.accname
						newrequest.accno = user.accno
						newrequest.level = user.level
						newrequest.save();

						newreq = Newrequest(request=newrequest, level=newrequest.level)
						newreq.save()

						messages.success(request, 'Request has been placed')
						return redirect(dashboard)
				else:
					messages.error(request, 'Incorrect Pincode')
					return redirect(dashboard)
			else:
				messages.error(request, 'Please edit your bank account details on your profile page')
				return redirect(dashboard)
		else:
			messages.error(request, 'Please Sign in')
			return redirect(index)
	else:
		return redirect(index)

def editprofile(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			user = User.objects.get(username=request.user.username)

			firstname = request.POST['first_name']
			lastname = request.POST['last_name']
			email = request.POST['email']
			phoneno = request.POST['phoneno']

			if not firstname or not lastname or not email or not phoneno:
				messages.error(request, 'Please fill the required filled')
				return redirect(profile)
			else:
				bankname = request.POST['bankname']
				accname = request.POST['accname']
				accno = request.POST['accno']
				
				if not accname or not accno or bankname=='null':
					messages.error(request, 'Please enter bank details')
					return redirect(profile)
				else:
					user.first_name = firstname
					user.last_name = lastname
					user.email = email
					user.phoneno = phoneno
					user.bankname = bankname
					user.accname = accname
					user.accno = accno

					currentpassword = request.POST['currentpassword']
					newpassword = request.POST['newpassword']
					newpassword2 = request.POST['newpassword2']
					

					if currentpassword and newpassword:

						if user.check_password(currentpassword):
							if newpassword == newpassword2:
								user.set_password(newpassword)
								user.save()
							else:
								messages.error(request, 'Passwords choosen does not match each other')
								return redirect(profile)
						else:
							messages.error(request, 'Password mismatch')
							return redirect(profile)


					# Check for pincode change
					currentpincode = request.POST['currentpincode']
					newpincode = request.POST['newpincode']
					newpincode2 = request.POST['newpincode2']

					if currentpincode:
						if newpincode == newpincode2:
							if newpincode:
								user.pincode = newpincode
								user.save()
								messages.success(request, 'Pincode has been changed')
								return redirect(profile)
							else:
								messages.error(request, 'Pincode is empty')
								return redirect(profile)
						else:
							messages.error(request, 'Pincode 1 does not match pincode 2')
							return redirect(profile)

					user.save()
					messages.success(request, 'Details updated')
					return redirect(profile)
		else:
			messages.error(request, 'Please Sign in')
			return redirect(index)
	else:
		return redirect(index)


# DJANGO NAIVE CODES END HERE



# REST API CODES
class Usernames(APIView):

	def get(self, request):
		objs = User.objects.all()
		serializer = UserSerializer(objs, many=True)
		return Response(serializer.data)

	permission_classes = ( IsAuthenticated, )

class AdminProcessRequest(APIView):

	def get(self, request, pk):
		if request.session['adminuser']:
			objs = Request.objects.get(pk=pk)
			objs.adminstatus = True
			objs.save()

			return Response(True)
		else:
			messages.error(request, 'Please login before further action')
			return Response(False)

class StaffProcessRequest(APIView):

	def get(self, request, pk):
		if request.session['staffuser']:
			objs = Request.objects.get(pk=pk)
			objs.staffstatus = True
			objs.save()

			return Response(True)
		else:
			messages.error(request, 'Please login before further action')
			return Response(False)


class SuspendStaff(APIView):

	def get(self, request, pk):
		if request.session['adminuser']:
			objs = Staff.objects.get(pk=pk)
			objs.status = 'suspend'
			objs.save()

			return Response(True)
		else:
			messages.error(request, 'Please login before further action')
			return Response(False)


class AllowStaff(APIView):

	def get(self, request, pk):
		if request.session['adminuser']:
			objs = Staff.objects.get(pk=pk)
			objs.status = 'active'
			objs.save()

			return Response(True)
		else:
			messages.error(request, 'Please login before further action')
			return Response(False)


class ClearRequests(APIView):

	def get(self, request, level):
		if request.session['staffuser']:
			Newrequest.objects.filter(level=level).delete()

			return Response(True)
		else:
			messages.error(request, 'Please login before further action')
			return Response(False)