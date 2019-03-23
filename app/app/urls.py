"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework import routers
from lastcard.views import UserViewSet, CardViewSet, login
from django.conf.urls import url, include
from django.conf.urls.static import static

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'login', login),
    url(r'^', include(router.urls)),
] + static('qrcodes', document_root=settings.QRCODE_IMAGES_PATH)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
