from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('verify-payment/mpesa-callback/', views.mpesa_callback, name='mpesa_callback'), # Webhook callback route
    path('earning/', views.dashboard, name='dashboard'),
]