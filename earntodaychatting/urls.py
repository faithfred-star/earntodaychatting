from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # --- FIXED: Changed 'join' to 'urls' ---
    path('admin/', admin.site.urls), 
    
    path('', include('accounts.urls')), 
]