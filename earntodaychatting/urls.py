from django.contrib import admin
from django.urls import path
from accounts import views  # Make sure your accounts views are imported

urlpatterns = [
    path('admin/', admin.site.split),
    path('', views.home, name='home'),
    # --- ADD THIS LINE RIGHT HERE ---
    path('register/', views.register, name='register'), 
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('earning/', views.dashboard, name='dashboard'),
]