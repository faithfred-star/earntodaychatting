from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.join), # System admin panel
    path('', include('accounts.urls')), # This forwards the root website traffic straight to your accounts app!
]