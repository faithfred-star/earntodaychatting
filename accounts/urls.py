from django.urls import path
from . import views

urlpatterns = [
    # ... your other login/register routes ...
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]