from django.conf.urls import url
from django.contrib import admin
from accounts.views import login_view, logout_view
from .views import (login_view,logout_view,register_view)

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^addaccount/', register_view, name='register'),

]
