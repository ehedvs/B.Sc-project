import datetime
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Certificate, Student, AcademicHistory, Profile
from .resources import StudentResource, AcademicalResource, CertificateResource
from django.contrib import messages
from tablib import Dataset
from django.utils import timezone
from .forms import AcademicHistoryForm, ProfileUpdateForm, ExapleForm, update_dept,StudentForm
from django.utils import timezone
from .filter import AcademicFilter, StudentFilter
from datetime import date
from django.contrib.auth.decorators import login_required
from accounts.decorators import registrar_staff, allowed_users
from accounts.models import RegistrarStaff, RegistrarAdmin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer, ProfileSerializer, CertificateSerializer
from super_admin import signals
from registrar_admin.models import Request
from django.forms.models import modelformset_factory

# -------------------------------
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from graduates import serializers


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def index(request):
    status = "pending"
    uni = RegistrarStaff.objects.get(user = request.user).university
    admin = RegistrarAdmin.objects.get(university=uni)
    if Request.objects.filter(sender=admin)[0:1]:
        sub = Request.objects.filter(sender=admin)[0:1].values('status')[0]
        status= sub['status']
    status = "approved"
    students = Student.objects.all().count()
    acadamic_historys = AcademicHistory.objects.all().count()
    profile = Profile.objects.filter(image='default.png').count()
    #profile_changed =100-(profile/students)*100

    #certificates = Certificate.objects.filter(image='default.png')
    context = {
        'students': students,
        'acadamic_historys': acadamic_historys,
        # 'profile_changed':profile_changed,
        'profile': profile,
        'status':status
    }
    return render(request, 'graduates/home.html', context)

def student_update(request):
    user = request.user
    student = Student.objects.filter(created_by=user)
    StudentForm = update_dept(user)
    StudentFormset = modelformset_factory(Student, form=StudentForm, extra=0)
    formset = StudentFormset(request.POST or None, queryset=Student.objects.filter(
        created_by=user, school__isnull=True))
    
    if formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()

    context = {
        'formset': formset,
        'no_formset':len(formset.forms)
    }
    return render(request, 'graduates/school&dept_update.html', context)

def school_department(request, id):
    student = Student.objects.get(id=id)
    user = request.user
    if request.method == 'POST':
        form = StudentForm(user,request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/graduates/student/')

    else:
        form = StudentForm(user,instance=student)
    context = {
        'form': form
    }
    return render(request, 'graduates/school_dept.html', context)




def request_approved_checker(request):
    status = "pending"
    uni = RegistrarStaff.objects.get(user = request.user).university
    admin = RegistrarAdmin.objects.get(university=uni)
    if Request.objects.filter(sender=admin)[0:1]:
        sub = Request.objects.filter(sender=admin)[0:1].values('status')[0]
        status= sub['status']
    return HttpResponse(status)

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
    deletion_number = students.count()
    if request.method == 'POST':
        students.delete()
        return redirect('/graduates/status/')
    context = {'students': students, 'myfilter': myfilter,
      'deletion_number': deletion_number}
    return render(request, 'graduates/student_status.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def student_graduation_result(request):
    graduates = Certificate.objects.all()
    context ={
        'graduates':graduates
    }
    return render(request, 'graduates/student.graduation_result.html', context)


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

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def search_graduation(request):
    if request.GET:
        search_term = request.GET['date']
        num = Certificate.objects.filter( uploaded_date = search_term).count()
        

    context = {
        'search_term': search_term,
        'num': num

    }
    return render(request, 'graduates/delete_graduates.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['registrar_staff'])
def delete_graduates(request, date):

    if request.method == 'POST':
        num = Certificate.objects.filter(uploaded_date=date)
        if num:
            num.delete()
            messages.success(request, "successfully deleted")
            return redirect('/graduates/graduates')
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
    return render(request, 'graduates/navbar.html')


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
        now = datetime.date.today()
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
        now = timezone.now()
        new_student = request.FILES['myfile']
        imported_data = dataset.load(new_student.read(), format='xlsx')

        result = student_resource.import_data(
            dataset,
            dry_run=True,
            raise_errors=True,
            uploaded_date=now,

        )
        if result.has_errors():
            messages.error(request, 'Uh oh! Something went wrong....')

        else:
            student_resource.import_data(
                dataset,
                dry_run=False,
                uploaded_date=now,

            )
            messages.success(request, 'You have uploaded successfully!')
            return redirect('/graduates/graduation_result')
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

# certificate generation


def certificate_generation(request):
    certificates = Student.objects.all()
    context = {
        'certificates': certificates,

    }
    return render(request, 'graduates/certificate_generation.html', context)

# single certificate generation


def single_certificate(request, *args, **kwargs):
    id = kwargs.get('id')
    student = get_object_or_404(Student, id=id)

    template_path = 'graduates/single_certificate.html'
    context = {'student': student}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display
    response['Content-Disposition'] = 'filename="%s.pdf"' % student
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
    signals.certificate_generated_signal.send(
        instance.__class__, instance=instance, request=request)
    return response

    # multiple certificate


def multiple_certificate(request):
    students = Student.objects.all()
    template_path = 'graduates/multiple_certificate.html'
    context = {'students': students}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display
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
    signals.certificates_generated_signal.send(
        instances.__class__, instances=instances, request=request)
    return response

#serialize student profiles
@api_view(['GET'])
def get_profiles(request):
    students = Profile.objects.all()
    pro_serializer = ProfileSerializer(students, many=True)
    return Response(pro_serializer.data)

#serialize student profile
@api_view(['GET'])
def get_profile(request, id):
    student = Profile.objects.get(student=id)
    serializer = ProfileSerializer(student, many=False)
    return Response(serializer.data)


# certificates serializer
@api_view(['GET'])
def get_certificates(request):
    students = Certificate.objects.all()
    pro_serializer = CertificateSerializer(students, many=True)
    return Response(pro_serializer.data)

# certificate serializer
@api_view(['GET'])
def get_certificate(request, id):
    student = Certificate.objects.get(student=id)
    serializer = CertificateSerializer(student, many=False)
    return Response(serializer.data)

