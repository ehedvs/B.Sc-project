from django.urls import path
from.import views
app_name = 'registrar_admin'
urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('faculty/',views.faculty, name='faculty'),
    path('program/', views.program, name='program'),
    path('account/', views.createAccount, name='account'),
    path('user_profile/', views.useProfile, name='user_profile'),
    path('send_request/', views.send_request, name='send_request'),
    path('delete_request/<int:id>/', views.delete_request, name='delete_request'),

]