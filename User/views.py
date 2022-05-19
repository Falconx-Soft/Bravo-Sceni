from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CutomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from .models import*
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

# Create your views here.
@login_required(login_url='login')
def home(request):
	return render(request,'User/home.html')

def loginUser(request):

	if request.user.is_authenticated:
		return redirect('home')
	msg = None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			user = User.objects.get(username=username)
			user = authenticate(request, username=username, password=password) # check password

			if user is not None:
				login(request, user)
				return redirect('home')
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

def get_products(request):
	products_obj = products.objects.filter(user=request.user)
	context={
		'products':products_obj
	}
	return render(request,'User/products.html',context)

def add_products(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		quantity = request.POST.get('quantity')
		product_obj = products.objects.create(name=name,image=request.FILES['image'],user=request.user,quantity=quantity)
		product_obj.save()
		return redirect('products')
	return render(request,'User/add_products.html')

def delete_products(request,id):
	products_obj = products.objects.get(id=id)
	products_obj.delete()
	return redirect('products')

def edit_products(request,id):
	products_obj = products.objects.get(id=id)
	if request.method == 'POST':
		name = request.POST.get('name')
		quantity = request.POST.get('quantity')
		products_obj.name = name
		products_obj.quantity = quantity
		if request.FILES.get('image'):
			products_obj.image = request.FILES['image']
		products_obj.save()
		return redirect('products')
	context={
		'product' : products_obj
	}
	return render(request,'User/edit_products.html',context)
