from django.urls import path
from . import views

urlpatterns = [
    path('registration_confirmation', views.ConfirmEmail.as_view(), name='confirm_email'),
    path('user/<str:username>', views.UserProfile.as_view(), name='user_profile'),
    path('response/accept/<int:pk>', views.accept_response, name='accept_response'),
    path('response/delete/<int:pk>', views.delete_response, name='delete_response'),
]
