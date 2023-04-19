from django.urls import path
from .views import SearchResults, Reviews, ReviewsInfo, PopularCourses



urlpatterns = [
    path('search/', SearchResults.as_view()),
    path('popular-courses/', PopularCourses.as_view()),
    path('reviews-info/', ReviewsInfo.as_view()),
    path('reviews/', Reviews.as_view()),
]