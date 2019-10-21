from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from .models import User, Sponsorship, Request, Newrequest, Complain, Notification
import django
from jimcontrol.models import Staff, Registrationcode, AdminNotification, AdminUser, Agent
import random

from django.core.mail import send_mail

# Rest-api framework modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProcessingRequestSerializer
from rest_framework.permissions import IsAuthenticated


# Searching with django
# Model.objects.filter(username__icontains=search_keyword)


def index(request):
	if request.user.is_authenticated:
		return render(request, 'index/intro.html', {
			'title': 'Jimnet: Introduction to Jimnet',
			'user': User.objects.get(username=request.user.username)
		})
	else:
		return render(request, 'index/intro.html', {
			'title': 'Jimnet: Introduction to Jimnet'
		})

# login handler
def signin(request):
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
				return redirect(signin)
		else:
			messages.error(request, 'Invalid Login')
			return redirect(signin)

	# if the request is not a post
	else:
		logout_user(request)
		return render(request, 'index/login.html', {
			'title': 'Jim Networking Business',
			'page': 'login'
		})

def logout(request):
	logout_user(request)
	return redirect(signin)


# counter = 0
def dateback(referral):
	# if counter < 5:
	# 	global counter # To specify the variable 'counter is the general one'
	# 	counter+=1
	# else:
	# 	counter = 0;
	# 	return;
	if referral =='Jimnet':
		sponsorObj = User.objects.get(username='Jimnet')
		if sponsorObj.network < 1111110:
			if sponsorObj.network >= 111110:
				sponsorObj.network += 1;
				sponsorObj.balance += 5;
				sponsorObj.totearning += 5;
				sponsorObj.level = leveldeterminant(sponsorObj.username)
				sponsorObj.save()

			else:
				# print('Paying', sponsorObj.username,'#10')
				sponsorObj.network += 1;
				sponsorObj.balance += 10;
				sponsorObj.totearning += 10;
				sponsorObj.level = leveldeterminant(sponsorObj.username)
				sponsorObj.save()

		else:
			sponsorObj.network += 1;
			sponsorObj.save();

		return;
	else:
		# Trying to pay the sponsor of the referal=referal
		nextsponsorObj = Sponsorship.objects.get(member=referral)

		# Grabbing the sponsor_object of the referal of the currently paid person
		sponsorObj = User.objects.get(username=nextsponsorObj.sponsor.username)

		# checking if the sponsorObj's acount is booked
		if sponsorObj.accstatus=='Booked':
			dateback(sponsorObj.sponsor)
			return;

		if sponsorObj.network < 1111110:
			if sponsorObj.network >= 111110:
				sponsorObj.network += 1;
				sponsorObj.balance += 5;
				sponsorObj.totearning += 5;
				sponsorObj.level = leveldeterminant(sponsorObj.username)
				
			else:
				# print('Paying', sponsorObj.username,'#10')
				sponsorObj.network += 1;
				sponsorObj.balance += 10;
				sponsorObj.totearning += 10;
				sponsorObj.level = leveldeterminant(sponsorObj.username)

			sponsorObj.save()
		else:
			# this runs if the user has completed the levels i.e 1,000,000 referrals
			sponsorObj.network += 1;
			sponsorObj.save()

		if nextsponsorObj.sponsor.username != 'Jimnet':
			dateback(nextsponsorObj.sponsor.username)
		else:
			return;

def leveldeterminant(username):
	# print('usre:', username)
	user = User.objects.get(username=username)
	initiallevel = user.level
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
				levelcheckerandmessage(user, initiallevel, level)
				return level
		if cal:
			level = 2
			if user.network >= 1000 and user.network < 10000:
				level = 3
				levelcheckerandmessage(user, initiallevel, level)
				return level
			elif user.network >= 10000 and user.network<100000:
				level = 4
				levelcheckerandmessage(user, initiallevel, level)
				return level
			elif user.network >=100000 and user.network<10000000:
				level = 5
				levelcheckerandmessage(user, initiallevel, level)
				return level
			elif user.network >= 10000000:
				level = 6
				levelcheckerandmessage(user, initiallevel, level)
				return level

	levelcheckerandmessage(user, initiallevel, level)		
	return level;


def treeboy(user_obj):

	li = Sponsorship.objects.filter(sponsor=user_obj) # list of user_obj sponsorship
	if li:
		for s in li:
			member = s.member
			# print('sponsor: {}, member: {}'.format(s.sponsor.username, member))
			tree.append([ member, s.sponsor.username]) # set sponsor and the person sponsored
			if Sponsorship.objects.filter(sponsor=User.objects.get(username=member)):
				treeboy(User.objects.get(username=member))

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
				if referral!='Jimnet':
					if not User.objects.filter(username=referral): #check if the referer exist
						messages.error(request, "Sponsor doesn't exist, please check letter case")
						return redirect(register)

				# Check if password 1 match password 2
				if not request.POST['password']==request.POST['password2']:
					messages.error(request, "Password 1 does not match password 2")
					return redirect(register)

				if not request.POST['pincode']==request.POST['pincode2']:
					messages.error(request, "Pincode 1 does not match pincode 2")
					return redirect(register)

				# Checking the registration code
				paymet = request.POST['paymet']
				if paymet=='code':
					regcode = request.POST['regcode'].upper().replace(' ', '')
					if regcode:
						if Registrationcode.objects.filter(code=regcode):
							if Registrationcode.objects.get(code=regcode).status:
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
						user.save()
						reg = Registrationcode.objects.get(code=regcode)
						reg.status = True;
						reg.save()

						user = authenticate(request, username=username, password=password)
						if user is not None:
							login_user(request, user)

							if username != 'Jimnet':
								# Checking if the sponsor's L1 is complete
								payUplines(referral, user) # referral is the person who brought you

							messages.success(request, 'Registration successful. Welcome '+username)
							return redirect(dashboard)
				elif paymet=='booking':
					# booking goes here
					if not request.POST['agent']:
						messages.error(request, 'Please choose an agent to pay to')
						return redirect(register)


					if not Agent.objects.filter(username=request.POST['agent']):
						messages.error(request, 'Agent does not exit')
						return redirect(register)

					user = form.save(commit=False)
					username = form.cleaned_data['username']
					password = form.cleaned_data['password']
					user.set_password(password)
					user.accstatus = 'Booked'
					user.regcode = generateBookingCode()
					user.agent = request.POST['agent']
					user.save()

					user = authenticate(request, username=username, password=password)
					if user is not None:
						login_user(request, user)

						messages.success(request, 'Registration successful. Welcome '+username+'. Your booking number is '+user.regcode)
						return redirect(dashboard)
				elif paymet=='card':
					#this user is stored in a session because his payment is yet to be approved
					request.session['newUser'] = {
						'username': request.POST['username'],
						'first_name': request.POST['first_name'],
						'last_name': request.POST['last_name'],
						'phoneno': request.POST['phoneno'],
						'email': request.POST['email'],
						'password': request.POST['password'],
						'pincode': request.POST['pincode'],
						'sponsor': request.POST['sponsor']
					}
					return redirect('https://paystack.com/pay/complete-jimnet-registraion')
				else:
					messages.error(request, "You have not selected any payment method")
					return redirect(register)
			else:
				messages.error(request, 'Please ensure to fill all field')
				return redirect(register)
	else:
		sponsor = request.GET.get('sponsor')
		if not sponsor:
			sponsor = 'Jimnet'

		return render(request, 'index/register.html', {
			'title': 'Sign Up today to Jim Networking Business',
			'sponsor': sponsor,
			'agents': Agent.objects.all(),
			'page': 'register'
		})

# Callback after payment
def completePayment(request):
	reference = request.GET.get('reference')
	if reference:
		if request.session['newUser']:
			if User.objects.filter(username=request.session['newUser']['username']):
				messages.error(request, 'Username has been taken. Your reference number is {}'.format(reference))
				return redirect(register)

			newMem = User()
			newMem.username = request.session['newUser']['username']
			newMem.first_name = request.session['newUser']['first_name']
			newMem.last_name = request.session['newUser']['last_name']
			newMem.phoneno = request.session['newUser']['phoneno']
			newMem.set_password(request.session['newUser']['password'])
			newMem.pincode = request.session['newUser']['pincode']
			newMem.sponsor = request.session['newUser']['sponsor']
			newMem.regcode = reference
			newMem.save();

			payUplines(newMem.sponsor, newMem)
			user = authenticate(request, username=newMem.username, password=request.session['newUser']['password'])
			request.session['newUser'] = {}
			login_user(request, user)
			
			messages.success(request, 'Registration successful')
			return redirect(dashboard)

		messages.success(request, 'Please send your reference number {} to the help email for your account activation'.format(reference))
		return redirect(signin)
	else:
		messages.error(request, 'Sorry, an error occured')
		return redirect(register)



# This pays all the from intermediate to the next 5 uplines
def payUplines(referral, user):
	username = user.username
	sponsorObj = User.objects.get(username=referral)
	# print('I love Mistura!')

	if Sponsorship.objects.filter(sponsor=sponsorObj, member=username):
		# print('Returning')
		# print('Sorry processing or processed') Stop process if the sponsorship exist
		return;

	if len(Sponsorship.objects.filter(sponsor=sponsorObj)) < 10:
		if sponsorObj.accstatus=='Booked':
			user.sponsor = sponsorObj.sponsor
			user.save()
			return payUplines(sponsorObj.sponsor, user)
			


		user.sponsor = referral
		user.save()

		# print('Paying',sponsorObj.username, '#20')
		sponsorObj.network += 1;
		sponsorObj.balance += 20;
		sponsorObj.totearning += 20;

		# Creating new sponsorship
		newSponsorship = Sponsorship(sponsor=sponsorObj, member=username)
		newSponsorship.save()

		# Updating the sponsor's level
		sponsorObj.level = leveldeterminant(referral)
		sponsorObj.save()
		

		# Rewarding for getting to level 1 within 14 days of registration
		if len(Sponsorship.objects.filter(sponsor=sponsorObj))==10:
			if qualifyforbonus(sponsorObj):
				sponsorObj.balance += 100
				sponsorObj.totearning += 100
				sponsorObj.save()
		

		if sponsorObj.username != 'Jimnet':
			dateback(referral)

		return;
	else:
		# Getting the down side of the sponsor
		nextsponsor = checksmallsponsorship( User.objects.get(username=referral) )
		# # print(nextsponsor)
		user.sponsor = nextsponsor
		user.save()

		
		sponsorObj = User.objects.get(username=nextsponsor)
		sponsorObj.network += 1;
		sponsorObj.balance += 20;
		sponsorObj.totearning += 20;
		# print('Paying {} #20'.format(sponsorObj.username))


		sponsorObj.level = leveldeterminant(nextsponsor)
		sponsorObj.save()


		# Rewarding for getting to level 1 within 14 days of registration
		if len(Sponsorship.objects.filter(sponsor=sponsorObj))==10:
			if qualifyforbonus(sponsorObj):
				sponsorObj.balance += 100
				sponsorObj.totearning += 100
				sponsorObj.save()

		# Creating new sponsorship
		newSponsorship = Sponsorship(sponsor=sponsorObj, member=username)
		newSponsorship.save()

		dateback(nextsponsor)

		return;


tree = [] # the tree name holder
def dashboard(request):
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user.username)

		mytree = treeboy(user)
		global tree   #To specify that the variable is for the one used in treeboy function
		tree = []
		if user.accstatus=='Booked':
			messages.error(request, 'This account is till booked, please activate this account to start earning')
		
		return render(request, 'index/home.html', {
			'title': 'Dashboard: Welcome to Jimnet',
			'user': user,
			'treeboy': mytree,
			'notification': Notification.objects.all().order_by('-date')[:4]
		})
	else:
		return redirect(signin)


def forgetpass(request):
	username = request.POST['username']
	if username:
		user_obj = User.objects.filter(username=username)
		if user_obj:
			user = User.objects.get(username=username)
			newpassword = str(random.randint(10000, 999999))
			user.set_password(newpassword)
			user.save()
			emailto = user.email

			message = 'Hello! Your new password is '+newpassword+'\n'+'Change your password to your taste on your next login.'+'\n'+'Please ignore this message if you did not try to reset your password on Jimnet.'

			res = send_mail("Jimnet password reset", message, "support@Jimnet.com",[emailto], fail_silently=True)
			# print('Emailing response', res)
			if res==1:
				messages.success(request, 'A mail has been sent to your email')
				return redirect(signin)
			else:
				messages.error(request, 'An error occured while sending mail, Please try again')
				return redirect(signin)
		else:
			messages.error(request, 'Username does not exist, please check letter case.')
			return redirect(signin)
	else:
		messages.error(request, 'Please fill the required field')
		return redirect(signin)


def profile(request):
	if request.user.is_authenticated:
		return render(request, 'index/profile.html', {
			'title': 'Profile: Welcome to Jimnet',
			'user': User.objects.get(username=request.user.username),
			'notification': Notification.objects.all().order_by('-date')[:4]
		})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(signin)

def paymenthistory(request):
	if request.user.is_authenticated:
		return render(request, 'index/paymenthistory.html', {
			'title': 'Payment History: Welcome to Jimnet',
			'user': User.objects.get(username=request.user.username),
			'notification': Notification.objects.all().order_by('-date')[:4],
			'history': Request.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date') 
		})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(signin)


def withdraw(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
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
						newrequest = Request()
						newrequest.user = user
						newrequest.amount = requestamount
						newrequest.balance = user.balance
						newrequest.bankname = user.bankname
						newrequest.accname = user.accname
						newrequest.accno = user.accno
						newrequest.level = user.level
						newrequest.save();

						bal = user.balance
						user.balance -= requestamount;
						user.save();

						newreq = Newrequest(request=newrequest, level=newrequest.level, bankname=newrequest.bankname)
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
			return redirect(signin)
	else:
		return redirect(signin)

def editprofile(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
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

					currentpassword = request.POST['currentpassword'].strip(' ')
					newpassword = request.POST['newpassword'].strip(' ')
					newpassword2 = request.POST['newpassword2'].strip(' ')
					

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
					currentpincode = request.POST['currentpincode'].strip(' ')
					newpincode = request.POST['newpincode'].strip(' ')
					newpincode2 = request.POST['newpincode2'].strip(' ')

					if currentpincode and newpincode:
						if newpincode == newpincode2:
							if user.pincode == currentpincode:
								user.pincode = newpincode
								user.save()
								messages.success(request, 'Pincode has been changed')
								return redirect(profile)
							else:
								messages.error(request, 'Pincode does not match')
								return redirect(profile)
						else:
							messages.error(request, 'Pincode 1 does not match pincode 2')
							return redirect(profile)

					# Ensuring its the account trying to change profile using password security
					if user.check_password(currentpassword):
						user.save()
						messages.success(request, 'Details updated')
						return redirect(profile)
					else: 
						messages.error(request, 'Please enter your current password before you have access to change profile.')
						return redirect(profile)
		else:
			messages.error(request, 'Please Sign in')
			return redirect(signin)
	else:
		return redirect(signin)


def complain(request):
	if request.method=='POST':
		email = request.POST['email'].strip(' ')
		subject = request.POST['subject'].strip(' ')
		body = request.POST['body'].strip(' ')

		if email and subject and body:
			complain = Complain()
			complain.email = email
			complain.subject = subject
			complain.body = body
			complain.staff = random.choice(Staff.objects.all())
			complain.date = django.utils.timezone.now()
			complain.save()

			messages.success(request, 'Complain has been sent, reply will be sent to your mail')
			return redirect(index)
		else:
			messages.error(request, 'Please fill all fields')
			return redirect(index)
		

	else:
		messages.error(request, 'Please fill the complain fields')
		return redirect(index)


def forgetpincode(request):
	if request.user.is_authenticated:
		newpincode = str(random.randint(100000,10000000))
		user = User.objects.get(username=request.user.username)
		user.pincode = newpincode
		user.save()

		message = 'Hello!, Your new pincode is '+newpincode+'\n'+'Please ignore this message if you did not try to reset payment pincode on Jimnet.'
		res = send_mail("Jimnet pincode reset", message, "ibdac2000@gmail.com",[user.email], fail_silently=True)
		
		if res==1:
			messages.success(request, 'A mail has been sent to you, please check to continue')
			return redirect(dashboard)
		else:
			messages.error(request, 'An error occured while processing')
			return redirect(dashboard)

	else:
		messages.error(request, 'Please sign in')
		return redirect(index)

def getContact(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			users_obj = []
			notfound = []
			users = request.POST['users'].strip(' ').replace(' ', '');
			users = users.split(',')
			if users:
				for user in users:
					if User.objects.filter(username=user):
						users_obj.append(User.objects.get(username=user))
					else:
						notfound.append(user)

				return render(request, 'index/search.html',{
					'title': 'Member search results',
					'user': User.objects.get(username=request.user.username),
					'users_obj': users_obj,
					'notfound': notfound
				})
			else:
				messages.error(request, 'No username was received')
				return redirect(dashboard)
		else:
			return redirect(dashboard)
	else:
		messages.error(request, 'Please sign in')
		return redirect(index)


# Generate booking code
def generateBookingCode():
	letters = ['a','b','c','d','e','f','g']
	code = 'Jim'+str(User.objects.count())+random.choice(letters)
	if User.objects.filter(regcode=code):
		generateBookingCode()
	else:
		return code;


# Check if user date of membership is less than a week
def qualifyforbonus(user):

	dateinterval = django.utils.timezone.now() - user.dateofmembership
	if dateinterval.days < 8:
		return True
	else:
		return False;



# mail messager
def mailmessager(subject, email, message):
	res = send_mail(subject, message, "support@Jimnet.com",[email], fail_silently=True)


def levelcheckerandmessage(user, initiallevel, level):
	if not initiallevel==level:
		adminnote = AdminNotification(message=user.username+' is now in level '+str(level))
		adminnote.save()

		# Alerting all admin users for new level entry
		for admin in AdminUser.objects.all():
			admin.note += 1
			admin.save()

		mailmessager('Your Jimnet account', user.email, 'Dear '+user.first_name+','+'\n'+'We would like to inform you that your account now have a new level. Welcome to level '+str(level)+'. More success your way! Best regards.')
		


# DJANGO NATIVE CODES END HERE



# REST API CODES
class Usernames(APIView):

	def get(self, request):
		objs = User.objects.all()
		serializer = UserSerializer(objs, many=True)
		return Response(serializer.data)

	# permission_classes = ( IsAuthenticated, )

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

class Deletepin(APIView):

	def get(self, request, pk):
		if request.session['adminuser']:
			if Registrationcode.objects.filter(pk=pk):
				Registrationcode.objects.get(pk=pk).delete()

				return Response(True)
			else:
				return Response(False)
		else:
			return Response(False)

class MarkComplain(APIView):
	def get(self, request, status, pk):
		if request.session['staffuser']:
			if Complain.objects.filter(pk=pk):
				complain = Complain.objects.get(pk=pk)
				if status=='read':
					complain.msgstatus = True
				elif status=='unread':
					complain.msgstatus = False
				else:
					return Response(False)

				complain.save()
				return Response(True)
			else:
				return Response(False)
		else:
			return Response(False)

class Checknotification(APIView):
	def get(self, request):
		if request.user.is_authenticated:
			user = User.objects.get(username=request.user.username)
			user.note = False
			user.save();

			return Response(True);
		else:
			return Response(False);

class Clearunreadalerts(APIView):
	def get(self, request):
		if request.session['adminuser']:
			admin = AdminUser.objects.get(username=request.session['adminuser'])
			admin.note = 0
			admin.save()

			return Response(True)
		else:
			return Response(False)

class ActivateMemberAccount(APIView):
	def get(self, request, pk):
		if request.session['agentuser']:
			idChecker = User.objects.filter(pk=pk)

			if not idChecker:
				# print('You are not the one in charge')
				return Response(False)
			else:
				user = User.objects.get(pk=pk)
				if request.session['agentuser']==user.agent:
					if Agent.objects.get(username=user.agent).balance < 100:
						return Response(False)

					# print('About to activate')
					user.accstatus = 'active'
					user.agent = 'null'
					user.save()
					payUplines(user.sponsor, user)
					# Taking out 100 from Agent's account
					agent = Agent.objects.get(username=request.session['agentuser'])
					agent.balance -= 100
					agent.save()
					return Response(True)
				else:
					# print('You are no longer assigned')
					return Response(False)
		else:
			# print('You are not logged in')
			return Response(False)


class Deleteagent(APIView):
	def get(self, request, pk):
		if request.session['adminuser']:
			if not Agent.objects.filter(pk=pk):
				messages.error(request, 'Agent does not exist')
				return Response(False)

			Agent.objects.get(pk=pk).delete()
			return Response(True)
		else:
			return Response(False)

class AgentBookings(APIView):
	def get(self, request, pk):
		if request.session['adminuser']:
			if not Agent.objects.filter(pk=pk):
				return Response(False)

			agentUsername = Agent.objects.get(pk=pk).username
			userdetails = {}
			container = []
			for user in User.objects.filter(agent=agentUsername):
				userdetails['username'] = user.username
				userdetails['id'] = user.pk
				userdetails['regcode'] = user.regcode

				container.append(userdetails)
				userdetails = {}

			return Response(container)

		else:
			return Response(False)

class DeleteBooking(APIView):
	def get(self, request, pk):
		if request.session['adminuser']:
			if not User.objects.filter(pk=pk):
				return Response(False)

			User.objects.get(pk=pk).delete()
			return Response(True)
		else:
			messages.error(request, 'Please login to continue')
			return Response(False)

class UpdateAgentBalance(APIView):
	def post(self, request, pk):
		if request.session['adminuser']:
			if Agent.objects.filter(pk=pk):
				agent = Agent.objects.get(pk=pk)
				agent.balance += int(request.data['balance'])
				agent.save()

				return Response(True)
			else:
				messages.error(request, 'Agent does not exist')
				return Response(False)
		else:
			messages.error(request, 'Please login to continue')
			return Response(False)

class Paymemberbyhand(APIView):
	def post(self, request, pk):
		if request.session['adminuser']:
			if User.objects.filter(pk=pk):
				member = User.objects.get(pk=pk)
				amount = int(request.data['amount'])
				if amount>member.balance:
					print('Sorry, you dont have up to that amount')
					return Response(False)
				else:
					member.balance -= amount
					member.save();
					newrequest = Request(user=member, amount=amount,staffstatus=True,adminstatus=True, balance=member.balance,bankname='Collected by hand',level=member.level)
					
					newrequest.save();

					print('Payment recorded!')
					return Response(True)

				return Response(True)
			else:
				messages.error(request, 'Agent does not exist')
				return Response(False)
		else:
			messages.error(request, 'Please login to continue')
			return Response(False)