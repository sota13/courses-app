from django.urls import path
from .views import OrderList, SingleOrder



urlpatterns = [
    path('', OrderList.as_view()),
    path('single-order/', SingleOrder.as_view()),
]