'''
Created on Feb 7, 2016

@author: meiordac
'''

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]