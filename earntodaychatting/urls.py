from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    # Change 'admin.site.split' to 'admin.site.urls'
    path('admin/', admin.site.urls),  
    
    path('', views.home, name='home'),
    path('register/', views.register, name='register'), 
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('earning/', views.dashboard, name='dashboard'),
]