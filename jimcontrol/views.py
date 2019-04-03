from django.shortcuts import render, redirect
from .forms import AdminUserForm, StaffUserForm
from django.contrib import messages
from .models import AdminUser, Staff, Registrationcode
from index.models import Request, User, Newrequest
import random;


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
					if request.POST['pincode']=='ladipo963':
						adminuser = form.save(commit=False)
						username = form.cleaned_data['username']
						password = form.cleaned_data['password']
						adminuser.password = jimhash(password)

						adminuser.save()
						request.session['adminuser'] = username
						messages.success(request, 'Registration successfull')
						return redirect(adminrequests)
					else:
						messages.error(request, 'Wrong entry')
						return redirect('/')
				else:
					# Ensuring the pincode given match an existing account for validation
					if AdminUser.objects.filter(pincode=request.POST['pincode']):
						adminuser = form.save(commit=False)
						username = form.cleaned_data['username']
						password = form.cleaned_data['password']
						adminuser.password = jimhash(password)

						adminuser.save()
						request.session['adminuser'] = username
						messages.success(request, 'Registration successfull')

						return redirect(adminrequests)
					else:
						messages.error(request, 'Wrong entry')
						return redirect('/')
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
			'title': 'Staff: Jim Money Staff Sign in'
		})


def staffrequests(request):
	if request.session.has_key('staffuser'):
		staffobj = Staff.objects.get(username=request.session['staffuser'])
		return render(request, 'index/staffrequests.html', {
			'title': request.session['staffuser']+': Members withdrawal requests',
			'author': 'staff',
			'user': staffobj,
			'requests': Request.objects.filter(level=staffobj.job).order_by('-pk'),
			'newrequest': Newrequest.objects.filter(level=staffobj.job)
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

					messages.error(request, 'Password has been updated')
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
			'title': request.session['staffuser'] +': Jim Money Members Details',
			'author': 'staff',
			'user': Staff.objects.get(username=request.session['staffuser']),
			'members': User.objects.all().order_by('-totearning')
		})
	else:
		return redirect(staffsignin)
def staffsignout(request):
	del request.session['staffuser']
	return redirect(staffsignin)


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
			return redirect('/')
	else:
		return render(request, 'index/adminlogin.html', {
			'title': 'Admin: Jim Money Admin Sign in'
		})

def adminrequests(request):
	if request.session.has_key('adminuser'):
		return render(request, 'index/adminrequests.html', {
			'title': 'Admin: Jim Money Members Withdrawal Request',
			'author': 'admin',
			'requests': Request.objects.all().order_by('-pk'),
			'unapproved': Request.objects.filter(adminstatus=False).order_by('-pk')
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
		if request.method=='POST':
			pincode = request.POST['pincode']
			number = int(request.POST['number'])
			
			if not pincode or not number:
				messages.error(request, 'Please fill the require fields')
				return redirect(adminGeneratePin)

			admin = AdminUser.objects.get(username=request.session['adminuser'])
			if pincode==admin.pincode:
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
				'pins': Registrationcode.objects.all().order_by('-pk')
			})
	else:
		messages.error(request, 'Please Sign in')
		return redirect(adminsignin)


def adminmembers(request):
	if request.session.has_key('adminuser'):
		return render(request, 'index/members.html', {
			'title': 'Admin: Jim Money Members Details',
			'author': 'admin',
			'members': User.objects.all().order_by('-totearning')
		})
	else:
		return redirect(adminsignin)

def createstaff(request):
	if request.session.has_key('adminuser'):
		if request.method=='POST':
			username = request.POST['username']
			usernameObj = Staff.objects.filter(username=username)

			# Checking if the choosen username has been used
			if usernameObj:
				messages.error(request, 'Username has been used')
				return redirect(createstaff)

			# Checking password and password2 equality
			if request.POST['password']==request.POST['password2']:
				form = StaffUserForm(request.POST)
				if form.is_valid():
					staffuser = form.save(commit=False)
					# staffuser.password = jimhash(request.POST['password'])
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
				'staffs': Staff.objects.all()
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
		return redirect('/')

def updatejob(request, pk):
	if request.session.has_key('adminuser'):
		if request.method=='POST':
			print('Requests')
			print(request.POST)
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
			currentpin = request.POST['currentpincode']
			newpin = request.POST['newpin']
			newpin2 = request.POST['newpin2']

			if currentpin or newpin:
				if newpin==newpin2:
					admin = AdminUser.objects.get(username=request.session['adminuser'])
					if currentpin==admin.pincode:
						admin.pincode = newpin
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
		return redirect('/')
	else:
		return redirect(adminGeneratePin)


def adminsignout(request):
	if request.session.has_key('adminuser'):
		del request.session['adminuser']
		return redirect(adminrequests)
	else:
		return redirect('/')


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
	return newvalue

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