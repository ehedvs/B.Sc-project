from django.urls import path
from. import views
app_name ='graduates'
urlpatterns = [

    path('', views.index, name='home'),
    path('upload/', views.upload, name='upload' ),
    path('certificate/', views.certificate, name='e-hedvs' ),
    path('academic/', views.acadamic_history, name='academic'),
    path('graduation/', views.graduation_result, name='graduation'),
    path('status/', views.student_status, name='status'),
    path('status_detail/<path:id>/', views.status_detail, name='status_detail'),
    path('certificate_generation/',views.certificate_generation, name='certificate_generation' ),
    path('file/',views.know, name='file' ),
    path('profile/<path:pk>/',views.profile, name='profile' ),
    path('search/', views.search, name='search'),
    path('delete/<str:date>/', views.delete_records, name='delete'),
    path('student/', views.studentdata, name='student'),
    path('single/<path:id>/',views.single_certificate, name='single_certificate'),
    path('multi/', views.multiple_certificate, name='multi'),
    path('image_api/', views.get_profiles),
    path('image_api/<path:id>/', views.get_profile),
    path('student_api/', views.get_certificates),
    path('student_api/<path:id>/', views.get_certificate),



    


    


]