from django.urls import path
from . import views

app_name ='super_admin'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.registration, name='register'),
    path('account/', views.createAccount, name='account'),
    path('user_profile/', views.useProfile, name='user_profile'),
]