"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from accounts.views import (login_view,logout_view,register_view)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^newsletter/', include("newsletter.urls", namespace='newsletter')),

    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^addaccount/', register_view, name='register'),
    # url(r'^', include("newsletter.urls", namespace='newsletter')),
    url(r'^newsletter/', include("accounts.urls", namespace='accounts')),
    # url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^newsletter/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    # url(r'^newsletter/$', post_create),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
