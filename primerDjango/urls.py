from cgitb import html
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('accounts.urls', namespace='users')),
    path('social/', include('social.urls', namespace='social')),
    

    #path('ruta-para-publicar/', views.mi_vista, name='mi-vista'),

    path('', HomeView.as_view(), name="home"),

    #path('notifications/', NotificationView.as_view(), name='notifications'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
