from django.urls import path
from .views import EditProfile, UpdateUserPassword





urlpatterns = [
    path('edit-profile/', EditProfile.as_view()),
    path('update-password/', UpdateUserPassword.as_view()),
]