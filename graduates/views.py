import datetime
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Student, AcademicHistory, Profile
from .resources import StudentResource, AcademicalResource, CertificateResource
from django.contrib import messages
from tablib import Dataset
from django.utils import timezone
from .forms import AcademicHistoryForm, ProfileUpdateForm, ExapleForm
from django.utils import timezone
from .filter import AcademicFilter,StudentFilter
from datetime import date




def index(request):
    return render(request,'graduates/home.html' )

def graduates(request):
   
    year = ExapleForm()
    graduates = Student.objects.all()
    graduateFilter = StudentFilter(request.GET, queryset=graduates)
    graduates = graduateFilter.qs
    context = {'graduates': graduates, 'graduateFilter':graduateFilter, 'year':year }
    return render(request, 'graduates/student_list.html', context)


def student_status(request):
    students = AcademicHistory.objects.all().order_by('-uploaded_date')
    myfilter = AcademicFilter(request.GET, queryset=students)
    students = myfilter.qs
    #student =myfilter.qs
    context = {'students': students, 'myfilter':myfilter}
    return render(request,'graduates/student_status.html', context)

def file_upload(request):
    return render(request,'graduates/file_upload.html')



def status_detail(request, id):
    #student_i = Student.objects.get(id=id)
    #name = AcadamicHistory.objects.get(student=student_id).student.first
    name =Student.objects.get(id=id)
    student = AcademicHistory.objects.filter(student=id)
    context = {'students':student, 'name':name}
    return render(request,'graduates/status_detail.html', context)

   
def registrar_staff(request ):
    students=Student.objects.all().count()
    context = {'students': students }
    return render(request, 'graduates/registrar_staff.html',context)




def search(request):
    if request.GET:
        search_term = request.GET['date']
        num = Student.objects.filter(registration_year=search_term).count()
       
    context = {
        'search_term':search_term,
        'num':num
        
    }
    return render(request, 'graduates/delete_students.html', context)

def delete_records(request, date):
    
    if request.method =='POST':
        num = Student.objects.filter(registration_year=date)
        if num :
            num.delete()
            messages.success(request, "successfully deleted")
            return redirect('/graduates/graduates')
        else:
            messages.warning(request, 'No records found with this selected dateeeee')
            return redirect('/graduates/graduates') 

        
       

    return render(request, 'graduates/delete_students.html')

 

def certificate(request):
    if 'q' in request.GET:
        q=request.GET['q']
        if q:
            
            try:
                graduate = Student.objects.get(id=q)
                if graduate:
                     return render(request, 'graduates/e-hedvs.html',{'student':graduate})

            except Student.DoesNotExist:
                return render(request, 'graduates/e-hedvs.html',
                {'search':q,
                'error_message':'Sorry no result found with a keyword you entered'
                })



           
        else:
            return render(request, 'graduates/e-hedvs.html')
        
       

       
        
    return render(request, 'graduates/e-hedvs.html')
   


def upload(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        dataset = Dataset()
        new_student = request.FILES['myfile']
        imported_data = dataset.load(new_student.read(), format='xlsx')
        unv = 1
        created_by = request.user.id
        registration_year = datetime.date.today()

        result = student_resource.import_data(
            dataset,
            dry_run=True, 
            raise_errors=True,  
            institution=unv, 
            created_by=created_by ,
            reg_year=registration_year 
              )
        if result.has_errors():
            messages.error(request, 'Uh oh! Something went wrong....')
    
        else:
            student_resource.import_data(
                 dataset, 
                 dry_run=False,
                 institution=unv, 
                 created_by=created_by,
                 reg_year=registration_year
                  )
            messages.success(request, 'You have uploaded the file  successfully!')
            return redirect('/graduates/graduates')
     
    return render(request, 'graduates/upload.html')






def acadamic_history(request):
    if request.method == 'POST':
        student_resource = AcademicalResource()
        dataset = Dataset()
        new_student = request.FILES['myfile']
        imported_data = dataset.load(new_student.read(), format='xlsx')
        now = timezone.now()
        uploaded_by = request.user.id

        result = student_resource.import_data(
            dataset,
            dry_run=True, 
            raise_errors=True,  
            uploaded_by=uploaded_by,
            uploaded_date=now
              )
        if result.has_errors():
            messages.error(request, 'Uh oh! Something went wrong....')
    
        else:
            student_resource.import_data(
                 dataset, 
                 dry_run=False,
                 uploaded_by=uploaded_by,
                 uploaded_date=now
                  )
            messages.success(request, 'You have uploaded successfully!')
     
    return render(request, 'graduates/acadamic_history.html')

def graduation_result(request):
     if request.method == 'POST':
        student_resource = CertificateResource()
        dataset = Dataset()
        new_student = request.FILES['myfile']
        imported_data = dataset.load(new_student.read(), format='xlsx')


        result = student_resource.import_data(
            dataset,
            dry_run=True, 
            raise_errors=True,  
            
              )
        if result.has_errors():
            messages.error(request, 'Uh oh! Something went wrong....')
    
        else:
            student_resource.import_data(
                 dataset, 
                 dry_run=False,
              
                  )
            messages.success(request, 'You have uploaded successfully!') 
     return render(request, 'graduates/graduation_result.html')



def profile(request, pk):
    profile = Profile.objects.get(student=pk)
    if request.method == 'POST':
        p_form = ProfileUpdateForm( request.POST, 
                           request.FILES, 
                           instance=profile)
        if p_form.is_valid:
            p_form.save()
            messages.success(request, f'The profile Upadated successfully!!')
            return redirect('/graduates/student')

    else:
        p_form = ProfileUpdateForm(instance=profile)


    context = {
     'p_form':p_form
        }

    return render(request, 'graduates/profile.html', context)

    
def toast(request):
    now= timezone.now()
    return HttpResponse(now)




def date(request):
    now = datetime.date.today().strftime(" %m/ %d/ %Y")
    context = {
        'example_form':ExapleForm(),
        'now':now
    }
    return render(request, 'graduates/date.html', context )


def table(request):
    return render(request, 'graduates/datatable.html')

def studentdata(request):
    graduates = Student.objects.all()
    context = {'graduates': graduates,  }
    return render(request, 'graduates/studentdata.html', context )



