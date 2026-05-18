from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    
    # --- ADD THIS LINE TO MATCH THE REDIRECTS ---
    path('dashboard/', views.dashboard, name='dashboard'),
]