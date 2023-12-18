from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardView.as_view(), name='home'),
    path('create', views.BulletinCreateView.as_view(), name='create_bulletin')
]
