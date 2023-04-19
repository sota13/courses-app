from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from course.models import Course
from instructor.models import Instructor
from .serializers import CoursesSerializer, InstructorListSerializer, ReviewSerializer, FeaturedInstructorSerializer, PopularCoursesSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()



class SearchResults(APIView):
    """
    List all  search results.
    """

    def get(self, request):
        query = request.GET.get('query', '')
        courses = Course.objects.filter(name__icontains=query, status='published')
        courses_serializer = CoursesSerializer(courses, many=True)
        instructors = Instructor.objects.filter(Q(user__userprofile__first_name__icontains=query) | Q(user__userprofile__last_name__icontains=query),approved=True)
        instructors_serializer = InstructorListSerializer(instructors, many=True)
        return Response( {"courses": courses_serializer.data, "instructors": instructors_serializer.data}, status=status.HTTP_200_OK)



class PopularCourses(APIView):
    """
    List all  popular courses.
    """

    def get(self, request):
        courses = Course.objects.filter(rating__gte=4, status='published')
        serializer = PopularCoursesSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ReviewsInfo(APIView):
    """
    Get general info about the platform reviews and rating.
    """

    def get(self, request):
        #featured_reviews
        featured_reviews = Review.objects.filter(is_featured=True)[0:2]
        serializered_reviews = ReviewSerializer(featured_reviews, many=True).data

        #featured_instructors
        featured_instructors = Instructor.objects.filter(rating__gte=4)[0:3]
        serializered_instructors = FeaturedInstructorSerializer(featured_instructors, many=True).data

        #rating and number of review
        reviews = Review.objects.all()
        num_reviews = len(reviews)
        total = 0
        rating = 0
        if num_reviews:
            for i in reviews:
                total += i.rating
            rating = total / num_reviews

        reviews_info = {
            "featured_reviews":serializered_reviews,
            "featured_instructors":serializered_instructors,
            "rating":rating,
            "num_reviews":num_reviews,
        }


        return Response(reviews_info, status=status.HTTP_200_OK)



class Reviews(APIView):
    """
    List all  reviews.
    """

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        reviewer = request.user
        data = request.data

        # 1 - Review already exists
        alreadyExists = Review.objects.filter(reviewer=reviewer).exists()
        if alreadyExists:
            content = {'detail': 'You are already have reviewed this paltform'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2 - No Rating or 0
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3 - Create review
        else:
            review = Review.objects.create(
                reviewer=reviewer,
                rating=data['rating'],
                comment=data['comment'],
            )

            
            serializerd_review = ReviewSerializer(review).data

            return Response(serializerd_review, status=status.HTTP_200_OK)

