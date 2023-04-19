from rest_framework import serializers
from .models import Order, OrderItem
from course.serializers import CoursePriceSerializer
from django.contrib.auth import get_user_model

User = get_user_model()



class OrderItemSerializer(serializers.ModelSerializer):
    # course = CoursePriceSerializer()
    course = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'course', 'paid_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'created_date', 'total_price', 'is_paid', 'payment_method']