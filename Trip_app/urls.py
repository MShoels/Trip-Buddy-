from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),                
    url(r'^create$', views.create),         
    url(r'^login$', views.login),           
    url(r'^dashboard$', views.dashboard),   
    url(r'^destroy$', views.destroy),       
    url(r'^trips/new$', views.newtrip),     
    url(r'^trips/(?P<id>\d+)/destroy$', views.destroy_trip),    
    url(r'^trips/(?P<id>\d+)/edit$', views.edit_trip),          
    url(r'^trips/update', views.update_trip),                   
    url(r'^trips/(?P<id>\d+)$', views.view),                    
    url(r'^trips/create$', views.create_trip),                  
    url(r'^trips/(?P<id>\d+)/join$', views.join),               
    url(r'^trips/(?P<id>\d+)/cancel$', views.cancel), 
]