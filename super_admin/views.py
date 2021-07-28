from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from super_admin.models import University
from accounts.models import RegistrarAdmin, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import AdminSignUpForm
from django.contrib.auth.decorators import login_required
from .forms import UniversityForm
from accounts.decorators import super_admin




#dashboar on super admin page
@login_required(login_url='accounts:login')
@super_admin
def dashboard(request):
    lists = University.objects.all().order_by('-id')
    total_unv = lists.count()
    users =RegistrarAdmin.objects.all().count()
    context = {'lists':lists , 'total_unv':total_unv, 'users':users}
    return render(request, 'super_admin/dashboard.html', context)

# register high educational institution
@login_required(login_url='accounts:login')
@super_admin
def registration(request):
    form = UniversityForm()
    if request.method=='POST':
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/super_admin/')
    context = {'form':form}
    return render(request, 'super_admin/register.html', context)



#create account for registrar admin
@login_required(login_url='accounts:login')
@super_admin
def createAccount(request):
    form = AdminSignUpForm()
    if request.method=='POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/super_admin/user_profile')

        else:
            messages.warning(request,'the two password doesnot match')
    context = {'form': form}
    return render(request, 'super_admin/account.html', context)

#user profile
@login_required(login_url='accounts:login')
@super_admin
def useProfile(request):
    lists = RegistrarAdmin.objects.all().order_by('-user_id')[:6]
    context = {'lists':lists}
    return render(request, 'super_admin/user_profile.html', context)



#update univeristy
def updateUnv(request, pk):
    univ = University.objects.get(id=pk)
    form = UniversityForm(instance=univ)
    if request.method=='POST':
        form = UniversityForm(request.POST, instance=univ)
        if form.is_valid():
            form.save()
            return redirect('/super_admin/')
    context = {'form':form}
    return render(request, 'super_admin/register.html', context)

#delete University
def deleteUnv(request, pk ):
    univ = University.objects.get(id=pk)
    if request.method == 'POST':
        univ.delete()
        return redirect('/super_admin/')
    context = {'univ':univ}
    return render(request, 'super_admin/delete.html', context)


#delet Registrar_admin
def deleteRegAdmin(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('/super_admin/user_profile')
    context = {'user':user}
    return render(request, 'super_admin/delete_user.html', context)