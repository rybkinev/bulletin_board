from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdsView.as_view(), name='home'),
    path('<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('create', views.AdCreateView.as_view(), name='create_ad'),
    path('<int:pk>/edit/', views.AdEditView.as_view(), name='update_ad'),
    # path('', , name='accept_response')
]
