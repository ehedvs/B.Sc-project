from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from web_users import views as e_hedvs
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', e_hedvs.web_user, name='certificate' ),
    path('accounts/', include('accounts.urls')),
    path('super_admin/', include('super_admin.urls')),
    path('registrar_admin/', include('registrar_admin.urls')),
    path('graduates/', include('graduates.urls')),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
     path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
      ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
          ),
          name='password_reset_confirm'),
     path('password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

