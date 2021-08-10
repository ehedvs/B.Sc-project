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
    faculties = Faculty.objects.all().order_by('-id')[0:3]
    programs = Program.objects.all().order_by('-id')[0:3]
        
    return render(request, 'registrar_admin/dashboard.html',{'faculties':faculties, 'programs':programs})
   
@login_required(login_url='accounts:login')
@registrar_admin
def faculty(request):
    faculties = Faculty.objects.all().order_by('-id')[0:5]
    form = FacultyForms()
    if request.method == 'POST':
        form = FacultyForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/registrar_admin')

    return render(request, 'registrar_admin/faculty.html', {'form':form, 'faculties':faculties})

@login_required(login_url='accounts:login')
@registrar_admin
def program(request):
   programs = Program.objects.all().order_by('-id')[0:5]
   program = ProgramForms()
   if request.method == 'POST':
        form = ProgramForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/registrar_admin')

   return render(request, 'registrar_admin/program.html', { 'program':program, 'programs':programs})


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
             
            #print(dir(form))
            print(univ)
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
    if request.method =='POST':
        subject = request.POST.get('subject')
        super_admin = get_user_model().objects.get(is_superuser=True)
        logged_user = request.user
        registrar_admin=RegistrarAdmin.objects.get(user=logged_user)
        Request.objects.create(sender=registrar_admin, reciever=super_admin, request=subject)
        #process_tasks()
        
        

    return render(request, 'registrar_admin/request.html')