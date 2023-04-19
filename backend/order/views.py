from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from course.models import Course, CartItem, EnrolledCourse
from .serializers import OrderSerializer
import math



class OrderList(APIView):
    """
    List all orders, and create order for multiple items
    """

    def get(self, request):
        page_size = 9
        requested_page = request.GET.get('page', '')
        if requested_page:
            try:
                page = int(requested_page)
                start = (page - 1) * page_size if page > 1 else 0
                end = page * page_size
                print(start)    
                print(page)
                print(end)
                orders = Order.objects.all()[start:end]
                orders_count = Order.objects.all().count()
                serializer = OrderSerializer(orders, many=True)
                paginated_response = {
                    "count":orders_count,
                    "page_size":page_size,
                    "num_pages":math.ceil(orders_count / page_size),
                    "results":serializer.data
                }
                return Response(paginated_response, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error':'invalid page number'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error':"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.all()
        orders_count = Order.objects.all().count()
        serializer = OrderSerializer(orders, many=True)
        paginated_response = {
            "count":orders_count,
            "page_size":page_size,
            "num_pages":math.ceil(orders_count / page_size),
            "results":serializer.data
        }
        return Response(paginated_response, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        data = request.data
        cart_items = data.get('cart_items')

        
        try:
            # (1) Create order

            order = Order.objects.create(
                user=user,
                payment_method=data.get('payment_method'),
                total_price=data.get('total_price'),
                is_paid=True
            )

            

            # (2) Create order items and set order to orderItem relationship then delete item from user cart
            for i in cart_items:
                course_id = i['course']['id']
                course = Course.objects.get(id=course_id)
                cart_item = CartItem.objects.get(id=i['id'])
                
                EnrolledCourse.objects.create(user=user, course=course, method='buying')
                

                paid_price = course.price - course.discount if course.discount_enabled and course.price else course.price

                OrderItem.objects.create(
                    course=course,
                    order=order,
                    paid_price=paid_price
                )

                cart_item.delete()

            

                
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Sorry something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

        
class SingleOrder(APIView):
    """
    create order for single item.
    """
    def post(self, request):
        user = request.user
        data = request.data
        course_id = data.get('course_id')
        payment_method=data.get('payment_method')
        total_price=data.get('total_price')

        
        try:

            # (1) Enroll user
            course = Course.objects.get(id=course_id)
            EnrolledCourse.objects.create(user=user, course=course, method='buying')


            # (2) Create order

            order = Order.objects.create(
                user=user,
                payment_method=payment_method,
                total_price=total_price,
                is_paid=True
            )

            # (3) Create order item and assign it to order

            OrderItem.objects.create(
                    course=course,
                    order=order,
                    paid_price=total_price
                )

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Sorry something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

        
