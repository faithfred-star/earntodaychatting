from django.urls import path
from . import views

urlpatterns = [
    # --- FIX: Ensure the empty path maps to your homepage function ---
    path('', views.home, name='home'), 
    
    # Your other routes
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]