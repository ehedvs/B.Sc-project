from django.http.response import HttpResponse
from super_admin.models import University
from django.shortcuts import redirect, render
from .forms import FacultyForms, ProgramForms
from. models import Faculty,Program, Request
from accounts.models import RegistrarStaff, RegistrarAdmin
from accounts.forms import StaffSignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from accounts.decorators import registrar_admin
from django.contrib.auth import get_user_model



@login_required(login_url='accounts:login')
@registrar_admin
def dashboard(request):
    logged_user = request.user
    logged_admin_univ=RegistrarAdmin.objects.get(user=logged_user).university
    print(logged_admin_univ)
    faculties = Faculty.objects.filter( university=logged_admin_univ).order_by('-id')[0:5]
    programs = Program.objects.filter(faculty__university = logged_admin_univ).order_by('-id')[0:5]
        
    return render(request, 'registrar_admin/dashboard.html',{'faculties':faculties, 'programs':programs})

@login_required(login_url='accounts:login')
@registrar_admin
def faculty(request):
    logged_user = request.user
    logged_admin_univ=RegistrarAdmin.objects.get(user=logged_user).university
    faculties = Faculty.objects.filter(university = logged_admin_univ).order_by('-id')[0:5]
    loged=request.user.id
    univ = RegistrarAdmin.objects.get(pk=loged).university
    form = FacultyForms()
    if request.method == 'POST':
        form = FacultyForms(request.POST, loged_user=univ)
        if form.is_valid():
            form.save()
            return redirect('/registrar_admin')

    return render(request, 'registrar_admin/faculty.html', {'form':form, 'faculties':faculties})

@login_required(login_url='accounts:login')
@registrar_admin
def program(request):
   programs = Program.objects.all().order_by('-id')[0:5]
   logged_univ = RegistrarAdmin.objects.get(user=request.user).university
   program = ProgramForms(logged_univ)
   if request.method == 'POST':
       program = ProgramForms(logged_univ, request.POST)
       if program.is_valid:
           program.save()
           return redirect('/registrar_admin')
      
   
   return render(request, 'registrar_admin/program.html', { 'program':program, 'programs':programs})


def delete_faculty(request, id):
    school = Faculty.objects.get(id=id)
    school.delete()
    return redirect('/registrar_admin')

#register registrar_staff
@login_required(login_url='accounts:login')
@registrar_admin
def createAccount(request):
    form = StaffSignUpForm()
    loged=request.user.id
    univ = RegistrarAdmin.objects.get(pk=loged).university_id
    #form.fields['university'].initial=univ


    if request.method=='POST':
        form = StaffSignUpForm(request.POST, loged_user=univ)
        if form.is_valid():
            form.save()
            return redirect('/registrar_admin/user_profile')

        else:
            messages.warning(request,'the two password doesnot match')
    context = {'form': form}
    return render(request, 'registrar_admin/account.html', context)


#user profile
@login_required(login_url='accounts:login')
@registrar_admin
def useProfile(request):
    logged_user = request.user
    univ = RegistrarAdmin.objects.get(user=logged_user).university
    lists = RegistrarStaff.objects.filter(university=univ).order_by('-user_id')[:6]
    context = {'lists':lists}
    return render(request, 'registrar_admin/user_profile.html', context)



# sending request to super_admin
def send_request(request):
    logged_user = request.user
    registrar_admin=RegistrarAdmin.objects.get(user=logged_user)
    requests = Request.objects.filter(sender=registrar_admin)[0:4]
    if request.method =='POST':
        subject = request.POST.get('subject')
        super_admin = get_user_model().objects.get(is_superuser=True)
        logged_user = request.user
        registrar_admin=RegistrarAdmin.objects.get(user=logged_user)
        Request.objects.create(sender=registrar_admin, reciever=super_admin, request=subject)
        #process_tasks()
        
        
    context ={
        'requests':requests
    }
    return render(request, 'registrar_admin/request.html', context)


def delete_request(request, id):
    rqst = Request.objects.get(id=id)
    rqst.delete()
    return redirect('/registrar_admin/send_request/')

