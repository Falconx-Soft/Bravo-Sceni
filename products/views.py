from multiprocessing import context
from django.shortcuts import render, redirect
from .models import*
from events.models import*
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def get_products(request):
	products_obj = products.objects.all()
	context={
		'products':products_obj
	}
	return render(request,'products/products.html',context)

@login_required(login_url='login')
def add_products(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			name = request.POST.get('name')
			quantity = request.POST.get('quantity')
			product_obj = products.objects.create(name=name,image=request.FILES['image'],quantity=quantity,quantity_left=quantity)
			product_obj.save()
			return redirect('products')
		return render(request,'products/add_products.html')
	else:
		return redirect('products')
	

@login_required(login_url='login')
def delete_products(request,id):
	if request.user.is_superuser:
		products_obj = products.objects.get(id=id)
		products_obj.delete()
	return redirect('products')

@login_required(login_url='login')
def edit_products(request,id):
	if request.user.is_superuser:
		products_obj = products.objects.get(id=id)
		if request.method == 'POST':
			name = request.POST.get('name')
			quantity = request.POST.get('quantity')
			products_obj.name = name
			products_obj.quantity_left += abs(int(quantity) - int(products_obj.quantity))
			products_obj.quantity = quantity
			if request.FILES.get('image'):
				products_obj.image = request.FILES['image']
			products_obj.save()
			return redirect('products')
		context={
			'product' : products_obj
		}
		return render(request,'products/edit_products.html',context)
	else:
		return redirect('products')

@login_required(login_url='login')
def view_product(request,id):
	products_obj = products.objects.get(id=id)
	event_products_obj = event_products.objects.filter(event_products=products_obj)
	context = {
		'product_details':event_products_obj,
		'products_obj':products_obj
	}
	return render(request,'products/view_product.html',context)