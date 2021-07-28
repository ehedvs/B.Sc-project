from django.contrib.auth import decorators
from django.http import HttpResponse, request
from django.shortcuts import redirect, render

def super_admin(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_superuser:
			return view_func(request, *args, **kwargs) 
		else:
			return render(request, 'accounts/404.html')

	return wrapper_func

def registrar_admin(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_registrar_admin:
			return view_func(request, *args, **kwargs) 
		else:
			return render(request, 'accounts/404.html')

	return wrapper_func


def registrar_staff(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_registrar_staff:
			return view_func(request, *args, **kwargs) 
		else:
			return render(request, 'accounts/404.html')

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group =None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return render(request, 'accounts/404.html')
		return wrapper_func

	return decorator	





# def unauthenticated_user(view_func):
# 	def wrapper_func(request, *args, **kwargs):
# 		if request.user.is_authenticated:
# 			return redirect('home')
# 		else:
# 			return view_func(request, *args, **kwargs)

# 	return wrapper_func





	