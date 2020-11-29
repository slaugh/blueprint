from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stateReport/', views.state_report, name='stateReport'),
    path('deviceState/<device_id>/', views.device_state, name='deviceState'),
    path('visualize/<device_id>/', views.visualize, name='visualize'),
]