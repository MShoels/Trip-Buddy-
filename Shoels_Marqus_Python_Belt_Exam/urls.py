from django.urls import path, include

urlpatterns = [
    path('', include('Trip_app.urls')),
]
