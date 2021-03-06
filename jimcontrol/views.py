from django.shortcuts import render, redirect
from .forms import AdminUserForm, StaffUserForm, AgentUserForm
from django.contrib import messages
from .models import AdminUser, Staff, Agent, Registrationcode, AdminNotification
from index.models import Request, User, Newrequest, Complain, Notification
import random;
from django.core.mail import send_mail
import django


def createadmin(request):
	if request.method=='POST':
		form = AdminUserForm(request.POST)
		if form.is_valid():

			# Checking if the username choose is in use
			if AdminUser.objects.filter(username=form.cleaned_data['username']):
				messages.error(request, 'Admin username is taken')
				return redirect(createadmin)

			# continue the process
			if request.POST['password']==request.POST['password2']: #checking is password1 equal password2

				# checking if the there is an admin account, so to give a default pincode for Admin account creation
				if len(AdminUser.objects.all())==0:

					# Validating the pincode given
					if request.POST['pincode']=='ladipo753':
						adminuser = form.save(commit=False)
						username = form.cleaned_data['username']
						password = form.cleaned_data['password']
						adminuser.password = jimhash(password)

						adminuser.save()
						request.session['adminuser'] = username
						messages.success(request, 'Registration successful')
						return redirect(adminrequests)
					else:
						messages.error(request, 'Wrong entry')
						return redirect('/signin')
				else:
					# Ensuring the pincode given match an existing account for validation
					if AdminUser.objects.filter(pincode=jimhash(request.POST['pincode'])):
						adminuser = form.save(commit=False)
						username = form.cleaned_data['username']
						password = form.cleaned_data['password']
						adminuser.password = jimhash(password)

						adminuser.save()
						request.session['adminuser'] = username
						messages.success(request, 'Registration successful')

						return redirect(adminrequests)
					else:
						messages.error(request, 'Wrong entry')
						return redirect('/signin')
			else:
				messages.error(request, 'Password choosen does not match')
				return redirect(createadmin)
		else:
			messages.error(request, 'Please fill the required filled')
			return redirect(createadmin)


	else:
		return render(request, 'index/newadmin.html', {
			'title': 'Admin: Create an Admin Account'
		})

def staffsignin(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		if not username or not password:
			messages.error(request, 'Please fill the required fields')
			return redirect(staffsignin)

		obj = Staff.objects.filter(username=username, password=password)
		if obj:
			if obj[0].status=='active':
				staff = Staff.objects.get(username=username)
				staff.lastlogin = django.utils.timezone.now()
				staff.save()
				request.session['staffuser'] = username
				return redirect(staffrequests)
			else:
				messages.error(request, 'This account has been suspended')
				return redirect(staffsignin)
		else:
			messages.error(request, 'Invalid login')
			return redirect(staffsignin)

	else:
		return render(request, 'index/stafflogin.html', {
			'title': 'Staff: Jim Net Staff Sign in'
		})


def staffrequests(request):
	if request.session.has_key('staffuser'):
		staffobj = Staff.objects.get(username=request.session['staffuser'])
		return render(request, 'index/staffrequests.html', {
			'title': request.session['staffuser']+': Members withdrawal requests',
			'author': 'staff',
			'user': staffobj,
			'requests': Request.objects.filter(level=staffobj.job).order_by('-pk'),
			'newrequest': Newrequest.objects.filter(level=staffobj.job).order_by('bankname')
		})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(staffsignin)

def staffprofile(request):
	if request.session.has_key('staffuser'):
		if request.method=='POST':
			currentpassword = request.POST['currentpassword']
			newpassword = request.POST['newpassword']
			newpassword2 = request.POST['newpassword2']

			if not currentpassword or not newpassword or not newpassword2:
				messages.error(request, 'Please fill all fields')
				return redirect(staffprofile)

			staff = Staff.objects.get(username=request.session['staffuser'])
			if currentpassword==staff.password:
				if newpassword2==newpassword:
					staff.password = newpassword
					staff.save()

					messages.success(request, 'Password has been updated')
					return redirect(staffrequests)
				else:
					messages.error(request, 'Password 1 does not match password2')
					return redirect(staffprofile)
			else:
				messages.error(request, 'Incorrect password')
				return redirect(staffprofile)
		else:
			return render(request, 'index/staffprofile.html', {
				'title': request.session['staffuser']+': Change Profile',
				'author': 'staff',
				'user': Staff.objects.get(username=request.session['staffuser'])
			})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(staffsignin)


def staffmembers(request):
	if request.session.has_key('staffuser'):
		return render(request, 'index/members.html', {
			'title': request.session['staffuser'] +': JimNet Members Details',
			'author': 'staff',
			'user': Staff.objects.get(username=request.session['staffuser']),
			'level0': User.objects.filter(level=0).order_by('-totearning'),
			'level1': User.objects.filter(level=1).order_by('-totearning'),
			'level2': User.objects.filter(level=2).order_by('-totearning'),
			'level3': User.objects.filter(level=3).order_by('-totearning'),
			'level4': User.objects.filter(level=4).order_by('-totearning'),
			'level5': User.objects.filter(level=5).order_by('-totearning'),
			'level6': User.objects.filter(level=6).order_by('-totearning'),
			'length': len(User.objects.all())-1
		})
	else:
		return redirect(staffsignin)

def staffcomplains(request):
	if request.session.has_key('staffuser'):
		staff = Staff.objects.get(username=request.session['staffuser'])
		return render(request, 'index/staffcomplains.html', {
			'title': request.session['staffuser'] +': JimNet Complains',
			'author': 'staff',
			'user': staff,
			'allcomplains': Complain.objects.all().order_by('msgstatus'),
			'mycomplains': Complain.objects.filter(staff=staff).order_by('msgstatus')
		})
	else:
		return redirect(staffsignin)

def admincomplains(request):
	if request.session.has_key('adminuser'):
		return render(request, 'index/adminmessage.html', {
			'title': 'Admin: JimNet Complains',
			'author': 'admin',
			'allcomplains': Complain.objects.all().order_by('msgstatus'),
			'notifications': Notification.objects.all().order_by('-date'),
			'user': AdminUser.objects.get(username=request.session['adminuser']),
			'alert': AdminNotification.objects.all().order_by('-date')
		})
	else:
		return redirect(adminsignin)

def alertAllUserForNewNote():
	for user in User.objects.all():
		user.note = True;
		user.save()


def sendmessage(request):
	if request.session.has_key('adminuser'):
		if request.method =='POST':
			message = request.POST['message'].strip(' ')
			if message:
				note = Notification(message=message)
				note.save();
				alertAllUserForNewNote();

				messages.success(request, 'Message has been sent')
				return redirect(admincomplains)

			else:
				messages.error(request, 'Please enter a message')
				return redirect(admincomplains)

	

	return redirect(adminsignin)


def staffsignout(request):
	del request.session['staffuser']
	return redirect(staffsignin)

def agentprofile(request):
	if request.session.has_key('agentuser'):
		if request.method=='POST':
			agent = Agent.objects.get(username=request.session['agentuser'])
			currentpassword = request.POST['currentpassword']
			newpassword = request.POST['newpassword']
			newpassword2 = request.POST['newpassword2']
			if not newpassword==newpassword2:
				messages.error(request, 'Password choosen does not match')
				return redirect(agentprofile)

			if not newpassword:
				messages.error(request, 'Password cannot be empty')
				return redirect(agentprofile)

			if not currentpassword==agent.password:
				messages.error(request, 'Password mismatch')
				return redirect(agentprofile)

			if newpassword == newpassword2:
				agent.password = newpassword
				agent.save()

				messages.success(request, 'Password update successful')
				return redirect(agentsignin)
		else:
			return render(request, 'index/agentprofile.html',{
				'title': 'Change your password',
				'author': 'agent',
				'agent': Agent.objects.get(username=request.session['agentuser'])
			})
	else:
		messages.error(request, 'Please login')
		return redirect(agentsignin)


def agentbooking(request):
	if request.session.has_key('agentuser'):
		agent = request.session['agentuser']

		return render(request, 'index/agentbookings.html',{
			'title': 'Your bookings',
			'bookings': User.objects.filter(agent=agent),
			'author': 'agent',
			'agent': Agent.objects.get(username=request.session['agentuser'])
		})
	else:
		messages.error(request, 'Please login')
		return redirect(agentsignin)

def agentsignin(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		if not username or not password:
			messages.error(request, 'Please fill the required fields')
			return redirect(agentsignin)

		
		if Agent.objects.filter(username=username, password=password):
			agent = Agent.objects.get(username=username)
			agent.lastlogin = django.utils.timezone.now()
			agent.save()
			request.session['agentuser'] = username
			return redirect(agentbooking)
		else:
			messages.error(request, 'Invalid login')
			return redirect(agentsignin)

	else:
		return render(request, 'index/agentlogin.html', {
			'title': 'Agent: Jim Net Agent Sign in'
		})

def agentsignout(request):
	del request.session['agentuser']
	return redirect(agentsignin)





def adminsignin(request):
	if request.method=='POST':
		username = request.POST['username']
		password = jimhash(request.POST['password'])

		adminUser = AdminUser.objects.filter(username=username, password=password)
		if adminUser:
			request.session['adminuser'] = username
			return redirect(adminrequests)
		else:
			messages.error(request, 'Invalid login')
			return redirect('/signin')
	else:
		return render(request, 'index/adminlogin.html', {
			'title': 'Admin: JimNet Admin Sign in'
		})

def adminrequests(request):
	if request.session.has_key('adminuser'):
		return render(request, 'index/adminrequests.html', {
			'title': 'Admin: JimNet Members Withdrawal Request',
			'author': 'admin',
			'requests': Request.objects.all().order_by('-pk'),
			'unapproved': Request.objects.filter(adminstatus=False).order_by('-pk'),
			'user': AdminUser.objects.get(username=request.session['adminuser'])
		})
	else:
		return redirect(adminsignin)

def adminprocessrequest(request, req_id):
	if request.session.has_key('adminuser'):
		id_obj = Request.objects.filter(pk=req_id)
		if id_obj:
			req = Request.objects.get(pk=req_id)
			req.adminstatus = True;
			req.save()
			return redirect(adminrequests)
		else:
			messages.error(request, 'Request Id does not exist.')
			return redirect(adminrequests)
	else:
		return redirect(adminsignin)

def adminGeneratePin(request):
	if request.session.has_key('adminuser'):
		admin = AdminUser.objects.get(username=request.session['adminuser'])
		if request.method=='POST':
			pincode = request.POST['pincode']
			number = request.POST['number']

			if str(number).isalpha():
				messages.error(request, 'Please enter a digit')
				return redirect(adminGeneratePin)

			number = int(number)
			
			if not pincode or not number:
				messages.error(request, 'Please fill the require fields')
				return redirect(adminGeneratePin)

			
			if jimhash(pincode)==admin.pincode:
				pins = [];
				for i in range(number):
					pin = regcode();

					regobj = Registrationcode(code=pin)
					regobj.save()
					pins.append(pin)

				return render(request, 'index/generatepin.html', {
					'title': 'Admin: Generate Jim Membership Reg. Code',
					'author': 'admin',
					'codes': pins,
					'pins': Registrationcode.objects.all().order_by('-pk')
				})

			else:
				messages.error(request, 'Incorrect Pincode')
				return redirect(adminGeneratePin)
		else:
			return render(request, 'index/generatepin.html', {
				'title': 'Admin: Generate Jim Membership Reg. Code',
				'author': 'admin',
				'pins': Registrationcode.objects.all().order_by('-pk'),
				'user': admin
			})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(adminsignin)


def adminmembers(request):
	if request.session.has_key('adminuser'):
		return render(request, 'index/adminmembers.html', {
			'title': 'Admin: JimNet Members Details',
			'author': 'admin',
			'level0': User.objects.filter(level=0).order_by('-totearning'),
			'level1': User.objects.filter(level=1).order_by('-totearning'),
			'level2': User.objects.filter(level=2).order_by('-totearning'),
			'level3': User.objects.filter(level=3).order_by('-totearning'),
			'level4': User.objects.filter(level=4).order_by('-totearning'),
			'level5': User.objects.filter(level=5).order_by('-totearning'),
			'level6': User.objects.filter(level=6).order_by('-totearning'),
			'length': len(User.objects.all())-1,
			'user': AdminUser.objects.get(username=request.session['adminuser']),
			'bookedUsers': User.objects.filter(accstatus='Booked')
		})
	else:
		return redirect(adminsignin)

def createstaff(request):
	if request.session.has_key('adminuser'):
		if request.method=='POST':
			username = request.POST['username'].strip(' ')
			usernameObj = Staff.objects.filter(username=username)

			# Checking if the choosen username has been used
			if usernameObj:
				messages.error(request, 'Username has been used')
				return redirect(createstaff)

			if not request.POST['password'].strip(' '):
				messages.error(request, 'Please choose a password')
				return redirect(createstaff)

			# Checking password and password2 equality
			if request.POST['password']==request.POST['password2']:
				form = StaffUserForm(request.POST)
				if form.is_valid():
					staffuser = form.save(commit=False)
					staffuser.lastlogin = django.utils.timezone.now()
					staffuser.save()

					request.session['staffuser'] = username
					messages.success(request, 'Staff account created')
					return redirect(createstaff)
				else:
					messages.error(request, 'Please fill all fields')
					return redirect(createstaff)
			else:
				messages.error(request, 'Password does not match')
				return redirect(createstaff)
		else:
			return render(request, 'index/newstaff.html', {
				'title': 'Admin: Create New Staff',
				'author': 'admin',
				'staffs': Staff.objects.all(),
				'agents': Agent.objects.all(),
				'user': AdminUser.objects.get(username=request.session['adminuser'])
			})
	else:
		return redirect(adminsignin)

def deletestaff(request, pk):
	if request.session.has_key('adminuser'):
		if Staff.objects.filter(pk=pk):
			user = Staff.objects.get(pk=pk)
			user.delete();

			messages.success(request, 'Staff account deleted')
			return redirect(createstaff)
		else:
			messages.error(request, 'Staff does not exist')
			return redirect(createstaff)
	else:
		return redirect('/signin')

def updatejob(request, pk):
	if request.session.has_key('adminuser'):
		if request.method=='POST':
			staff = Staff.objects.filter(pk=pk)
			if staff:
				obj = Staff.objects.get(pk=pk)
				obj.job = request.POST['job']
				obj.save();

				messages.success(request, obj.username+"'s job has been updated")
				return redirect(createstaff)
			else:
				messages.error(request, 'Staff does not exist')
				return redirect(createstaff)
		else:
			return redirect(createstaff)
	else:
		messages.error(request, 'An error occured')
		return redirect(createstaff)


def changepin(request):
	if request.session.has_key('adminuser'):
		if request.method=='POST':
			currentpin = request.POST['currentpincode'].strip(' ')
			newpin = request.POST['newpin'].strip(' ')
			newpin2 = request.POST['newpin2'].strip(' ')

			if currentpin and newpin:
				if newpin==newpin2:
					admin = AdminUser.objects.get(username=request.session['adminuser'])
					if jimhash(currentpin)==admin.pincode:
						admin.pincode = jimhash(newpin)
						admin.save()

						messages.success(request, 'Pincode has been changed')
						return redirect(adminGeneratePin)
					else:
						messages.error(request, 'Wrong pincode')
						return redirect(adminGeneratePin)
				else:
					messages.error(request, 'Pincode 1 does not match pincode 2')
					return redirect(adminGeneratePin)
			else:
				messages.error(request, 'Please fill all the fields')
				return redirect(adminGeneratePin)
		return redirect('/signin')
	else:
		return redirect(adminGeneratePin)

def changepassword(request):
	if request.session.has_key('adminuser'):
		if request.method=='POST':
			currentpassword = request.POST['currentpassword'].strip(' ')
			newpassword = request.POST['newpassword'].strip(' ')
			newpassword2 = request.POST['newpassword2'].strip(' ')

			if currentpassword and newpassword:
				if newpassword==newpassword2:
					admin = AdminUser.objects.get(username=request.session['adminuser'])
					if jimhash(currentpassword)==admin.password:
						admin.password = jimhash(newpassword)
						admin.save()

						messages.success(request, 'Password has been changed')
						return redirect(adminGeneratePin)
					else:
						messages.error(request, 'Wrong password')
						return redirect(adminGeneratePin)
				else:
					messages.error(request, 'Password 1 does not match password 2')
					return redirect(adminGeneratePin)
			else:
				messages.error(request, 'Please fill all the fields')
				return redirect(adminGeneratePin)
		return redirect('/signin')
	else:
		return redirect(adminGeneratePin)

def forgetpass(request):

	username = request.POST['username']
	if username:
		usernameObj = AdminUser.objects.filter(username=username)
		if usernameObj:
			newpassword = str(random.randint(300000,300000000))
			user = AdminUser.objects.get(username=username)
			user.password = jimhash(newpassword)
			user.save()

			message = 'Hello! Your new password is '+newpassword+'\n'+'Please ignore this message if you did not try to reset your password from JimNet'
			res = send_mail("JimNet password reset", message, "ibdac2000@gmail.com",[user.email])
			if res==1:
				messages.success(request, 'A mail has been set to your email box')
				return redirect(adminsignin)
			else:
				messages.error(request, 'An error occured while processing your request')
				return redirect(adminsignin)
		else:
			messages.error(request, 'Username does not exist')
			return redirect('/signin')
	else:
		messages.error(request, 'Please fill the field')
		return redirect(adminsignin)

def resetpincode(request):
	if request.session.has_key('adminuser'):
		newpincode = str(random.randint(300000,300000000))
		user = AdminUser.objects.get(username=request.session['adminuser'])
		user.pincode = jimhash(newpincode)
		user.save();

		message = 'Hello! Your new pincode is '+newpincode+'\n'+'Please ignore this message if you did not try to reset your pincode on JimNet'
		res = send_mail("JimNet pincode reset", message, "ibdac2000@gmail.com",[user.email])
		if res==1:
			messages.success(request, 'A mail has been set to your email box')
			return redirect(adminGeneratePin)
		else:
			messages.error(request, 'An error occured while processing your request')
			return redirect(adminsignin)
		return redirect(adminrequests)
	else:
		return redirect(adminsignin)


def adminsignout(request):
	if request.session.has_key('adminuser'):
		del request.session['adminuser']
		return redirect(adminrequests)
	else:
		return redirect('/signin')


def createagent(request):
	if request.session.has_key('adminuser'):
		form = AgentUserForm(request.POST)

		if form.is_valid():
			if not request.POST['password']==request.POST['password2']:
				messages.error(request, 'Passwords does not match')
				return redirect(createstaff)

			form.save()

			messages.success(request, 'Registration successful')
			return redirect(createstaff)
		else:
			messages.error(request, 'Please ensure to fill all fields')
			return redirect(adminsignin)
	else:
		return redirect(adminsignin)



# Password hasher
def jimhash(value):
	value = value.lower()
	jimkey = {
		'a': 'j',
		'b': 'k',
		'c': 'l',
		'd': 'm',
		'e': 'n',
		'f': 'p',
		'g': 'q',
		'h': 'r',
		'i': 's',
		'j': 'a',
		'k': 'b',
		'l': 'c',
		'm': 'd',
		'n': 'e',
		'o': 'f',
		'p': 'g',
		'q': 'z',
		'r': 'h',
		's': 'i',
		't': 'x',
		'u': 'w',
		'v': 'y',
		'w': 'u',
		'x': 't',
		'y': 'v',
		'z': 'q',
		'1': '5',
		'2': '3',
		'3': '8',
		'4': '6',
		'5': '7',
		'6': '1',
		'7': '4',
		'8': '9',
		'9': '0',
		'0': '2',
	}

	newvalue = value;
	for i in value:
		if i.isalpha() or i.isdigit():
			val = jimkey[i]
			newvalue = newvalue.replace(i, val)
	return str(newvalue)

# Registration code generator
def regcode():
	val = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

	result = 'J';
	result += str(random.randint(1, 9999))
	result += random.choice(val)+random.choice(val)+random.choice(val)
	
	regcodes = Registrationcode.objects.filter(code=result)

	if regcodes:
		return regcode()

	return result