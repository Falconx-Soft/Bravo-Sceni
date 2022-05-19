from django.shortcuts import render, redirect
from .models import*



def get_products(request):
	products_obj = products.objects.filter(user=request.user)
	context={
		'products':products_obj
	}
	return render(request,'products/products.html',context)

def add_products(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		quantity = request.POST.get('quantity')
		product_obj = products.objects.create(name=name,image=request.FILES['image'],user=request.user,quantity=quantity)
		product_obj.save()
		return redirect('products')
	return render(request,'products/add_products.html')

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
	return render(request,'products/edit_products.html',context)