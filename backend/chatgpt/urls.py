from django.urls import path
from .views import General, Code



urlpatterns = [
    path('general/', General.as_view()),
    path('code/', Code.as_view()),
]