from django.urls import path
from .views import *

urlpatterns = [
    # Спринт №1
    path('submitData/', PerevalAddAPI.as_view(), name='pereval-add'),  # Добавлен слэш
    # Спринт №2
    path('submitData/<int:pk>/', PerevalDetailAPI.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='pereval-detail'),
    path('submitData/', AuthEmailPerevalAPI.as_view({'get': 'list'}), name='auth-email-pereval'),
]
