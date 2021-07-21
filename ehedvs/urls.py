from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from graduates import views as e_hedvs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', e_hedvs.certificate, name='certificate' ),
    path('accounts/', include('accounts.urls')),
    path('super_admin/', include('super_admin.urls')),
    path('registrar_admin/', include('registrar_admin.urls')),
    path('graduates/', include('graduates.urls')),
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

