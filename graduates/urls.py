from django.urls import path
from. import views
app_name ='graduates'
urlpatterns = [

    path('', views.index, name='home'),
    path('school/', views.student_update, name='school'),
    path('dept/<path:id>/', views.school_department, name='dept'),
    path('request_approved_checker', views.request_approved_checker, name='request_approved_checker'),
    path('upload/', views.student_upload, name='upload' ),
    path('academic/', views.acadamic_history, name='academic'),
    path('status/', views.student_status, name='status'),
    path('status_detail/<path:id>/', views.status_detail, name='status_detail'),
    path('certificate_generation/',views.certificate_generation, name='certificate_generation' ),
    path('profile/<path:pk>/',views.profile, name='profile' ),
    path('search/', views.search, name='search'),
    path('search_graduates/', views.search, name='search_graduates'),
    path('delete/<str:date>/', views.delete_records, name='delete'),
    path('student/', views.studentdata, name='student'),
    path('single/<path:id>/',views.single_certificate, name='single_certificate'),
    path('multi/', views.multiple_certificate, name='multi'),
    path('image_api/', views.get_profiles),
    path('image_api/<path:id>/', views.get_profile),
    path('student_api/', views.get_certificates),
    path('student_api/<path:id>/', views.get_certificate),
    
]