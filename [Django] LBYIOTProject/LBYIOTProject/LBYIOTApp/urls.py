from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('getCurrentValue', views.getCurrentValue, name='getCurrentValue'),
    re_path(r'^(?P<url>.*)/$', views.errorPage, name='errorPage'),
]