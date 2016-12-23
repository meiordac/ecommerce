from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^logout/', views.logout, name='logout'),
    url(r'^login/', views.login, name='login')
    ]
