from django.urls import path, re_path
from LBYIOTApp import views

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    # path('getCurrentValue', views.getCurrentValue, name='getCurrentValue'),
    path('readerFunction', views.readerFunction, name='readerFunction'),
    path('switchlight/', views.switchlight, name='switchlight'),
    re_path(r'^(?P<url>.*)/$', views.errorPage, name='errorPage'),
]
