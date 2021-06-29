from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def super_admin(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_superuser:
			return view_func(request, *args, **kwargs) 
		else:
			return render(request, 'accounts/404.html')

	return wrapper_func

def registrar_admin(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_registrar_admin or request.user.is_registrar_staff :
			return view_func(request, *args, **kwargs) 
		else:
			return render(request, 'accounts/404.html')

	return wrapper_func


	