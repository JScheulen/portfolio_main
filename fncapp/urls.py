"""
URL configuration for fncapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from folioapp.views import calculadora, casa, get_number, currency_c, subir_archivo, tasa_cambio, actualizaPrecios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simulador/', calculadora, name='Calc'),
    path('resultado/',get_number, name='result'),
    path('',casa, name='home'),
    path('convert', currency_c, name='exchange'),
    path('success/',subir_archivo),
    path('exchange/', tasa_cambio, name='currency'),
    path('valormoneda/', actualizaPrecios, name='valormoneda')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
