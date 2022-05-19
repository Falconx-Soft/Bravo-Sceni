from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import*
from django.contrib.auth.hashers import check_password

# Create your views here.
@login_required(login_url='login')
def home(request):
	return render(request,'User/home.html')

def loginUser(request):

	if request.user.is_authenticated:
		return redirect('products')
	msg = None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			user = User.objects.get(username=username)
			user = authenticate(request, username=username, password=password) # check password

			if user is not None:
				login(request, user)
				return redirect('products')
			else:
				msg = 'User/Something is wrong'
		except:
			msg = 'User not recognized.'
	context = {
		'msg':msg
	}
	return render(request,'User/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def change_password(request):
	if request.method == 'POST':
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')
		user = request.user
		matchcheck= check_password(old_password, request.user.password)
		if matchcheck:
			user.set_password(new_password)
			user.save()
			return redirect('logout')
		else:
			context={
				'error':'Your old password is incorrect'
			}
			return render(request,'User/change_password.html',context)
	return render(request,'User/change_password.html')
