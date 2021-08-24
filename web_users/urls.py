from django.urls import path
from. import views
app_name ='web_users'
urlpatterns = [
    path('', views.website_user, name='website'),

]