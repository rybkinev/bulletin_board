from django.urls import path
from . import views

urlpatterns = [
    path('registration_confirmation', views.ConfirmEmail.as_view(), name='confirm_email'),
]
