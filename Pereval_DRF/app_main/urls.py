from django.urls import path, include
from .views import *

urlpatterns = [
    # Спринт №1
    path('submitData', PerevalAddAPI.as_view()),
    # Спринт №2
    path('submitData/<int:pk>/', PerevalDetailAPI.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('submitData/user__email=<str:email>', AuthEmailPerevalAPI.as_view({'get': 'list'})),
]