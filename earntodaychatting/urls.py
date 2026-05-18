from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Hand over all incoming traffic (including the homepage) to the accounts app
    path('', include('accounts.urls')), 
]