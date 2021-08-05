import datetime
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Student, AcademicHistory, Profile
from .resources import StudentResource, AcademicalResource, CertificateResource
from django.contrib import messages
from tablib import Dataset
from django.utils import timezone
from .forms import AcademicHistoryForm, ProfileUpdateForm, ExapleForm
from django.utils import timezone
from .filter import AcademicFilter, StudentFilter
from datetime import date
from django.contrib.auth.decorators import login_required
from accounts.decorators import registrar_staff, allowed_users
from accounts.models import RegistrarStaff
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer, ProfileSerializer
from super_admin import signals

#-------------------------------
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from graduates import serializers



@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def index(request):
    return render(request, 'graduates/home.html')


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def graduates(request):
    year = ExapleForm()
    graduates = Student.objects.all().order_by('-uploaded_date')
    graduateFilter = StudentFilter(request.GET, queryset=graduates)
    graduates = graduateFilter.qs
    context = {'graduates': graduates,
               'graduateFilter': graduateFilter, 'year': year}
    return render(request, 'graduates/student_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def student_status(request):
    students = AcademicHistory.objects.all().order_by('-uploaded_date')
    myfilter = AcademicFilter(request.GET, queryset=students)
    students = myfilter.qs
    #student =myfilter.qs
    context = {'students': students, 'myfilter': myfilter}
    return render(request, 'graduates/student_status.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def file_upload(request):
    return render(request, 'graduates/file_upload.html')


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def status_detail(request, id):
    #student_i = Student.objects.get(id=id)
    #name = AcadamicHistory.objects.get(student=student_id).student.first
    name = Student.objects.get(id=id)
    student = AcademicHistory.objects.filter(student=id)
    context = {'students': student, 'name': name}
    return render(request, 'graduates/status_detail.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def registrar_staff(request):
    students = Student.objects.all().count()
    context = {'students': students}
    return render(request, 'graduates/registrar_staff.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def search(request):
    if request.GET:
        search_term = request.GET['date']
        num = Student.objects.filter(registration_year=search_term).count()

    context = {
        'search_term': search_term,
        'num': num

    }
    return render(request, 'graduates/delete_students.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def delete_records(request, date):

    if request.method == 'POST':
        num = Student.objects.filter(registration_year=date)
        if num:
            num.delete()
            messages.success(request, "successfully deleted")
            return redirect('/graduates/student')
        else:
            messages.warning(
                request, 'No records found with this selected dateeeee')
            return redirect('/graduates/student')

    return render(request, 'graduates/delete_students.html')


def certificate(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:

            try:
                graduate = Student.objects.get(id=q)
                if graduate:
                    return render(request, 'graduates/e-hedvs.html', {'student': graduate})

            except Student.DoesNotExist:
                return render(request, 'graduates/e-hedvs.html',
                              {'search': q,
                               'error_message': 'Sorry no result found with a keyword you entered'
                               })

        else:
            return render(request, 'graduates/e-hedvs.html')

    return render(request, 'graduates/e-hedvs.html')


def know(request):
    user = request.user.id
    unv = RegistrarStaff.objects.get(user_id=user).university_id
    return HttpResponse(unv)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def upload(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        dataset = Dataset()
        new_student = request.FILES['myfile']
        imported_data = dataset.load(new_student.read(), format='xlsx')
        # logged_user
        user = request.user.id
        unv = RegistrarStaff.objects.get(user_id=user).university_id
        created_by = request.user.id
        registration_year = datetime.date.today()

        result = student_resource.import_data(
            dataset,
            dry_run=True,
            raise_errors=True,
            institution=unv,
            created_by=created_by,
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
            messages.success(
                request, 'You have uploaded the file  successfully!')
            return redirect('/graduates/student')

    return render(request, 'graduates/upload.html')

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
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
            return redirect('/graduates/status/')

    return render(request, 'graduates/acadamic_history.html')

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
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


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def profile(request, pk):
    profile = Profile.objects.get(student=pk)
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if p_form.is_valid:
            p_form.save()
            messages.success(request, f'The profile Upadated successfully!!')
            return redirect('/graduates/student')

    else:
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'graduates/profile.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def studentdata(request):
    graduates = Student.objects.all()
    context = {'graduates': graduates, }
    return render(request, 'graduates/studentdata.html', context)

#list of certificate
def student_certificates(request):
    students = Student.objects.all()
    context = {
        'students':students
    }
    return render(request, 'graduates/certificate_list.html', context)
    
# certificate generation
def certificate_generation(request):
    certificates = Student.objects.all()
    context = {
        'certificates':certificates,
        
    }
    return render(request, 'graduates/certificate_generation.html',context)

#single certificate generation

def single_certificate(request, *args, **kwargs):
    id = kwargs.get('id')
    student = get_object_or_404(Student, id=id)
    
    template_path = 'graduates/single_certificate.html'
    context = {'student': student}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if display 
    response['Content-Disposition'] = 'filename="%s.pdf"'%student
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    instance = student
    signals.certificate_generated_signal.send(instance.__class__, instance=instance, request=request)
    return response


    #multiple certificate
def multiple_certificate(request):
    students = Student.objects.all()
    template_path = 'graduates/multiple_certificate.html'
    context = {'students': students}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if display 
    response['Content-Disposition'] = 'filename="certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    instances = students
    signals.certificates_generated_signal.send(instances.__class__, instances=instances, request=request)
    return response

@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_profile(request, student):
    profile = Profile.objects.get(id=student)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

   
