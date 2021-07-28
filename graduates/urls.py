from django.urls import path
from. import views
app_name ='graduates'
urlpatterns = [
    path('', views.index, name='home'),
    path('upload/', views.upload, name='upload' ),
    path('graduates/', views.graduates, name='graduates' ),
    path('certificate/', views.certificate, name='e-hedvs' ),
    path('academic/', views.acadamic_history, name='academic'),
    path('graduation/', views.graduation_result, name='graduation'),
    path('status/', views.student_status, name='status'),
    path('status_detail/<path:id>/', views.status_detail, name='status_detail'),
    path('staff/',views.registrar_staff, name='staff' ),
    path('file/',views.file_upload, name='file' ),
    path('now/',views.toast, name='file' ),
    path('profile/<path:pk>/',views.profile, name='profile' ),
    path('data/', views.table,  name='data'),
    path('search/', views.search, name='search'),
    path('delete/<str:date>/', views.delete_records, name='delete'),
    path('student/', views.studentdata, name='student'),
    path('api/', views.get_profile, name='api'),
    


    


]