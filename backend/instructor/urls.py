from django.urls import path
from .views import (
    InstructorList,
    InstructorsRequestsList,
    RateInstructor,
    InstructorProfile,
    InstructorDashboard,
    ListingRequests,
    HandleListingRequest
)





urlpatterns = [
    path('', InstructorList.as_view()),
    path('<int:pk>/', InstructorProfile.as_view()),
    path('dashboard/<int:pk>/', InstructorDashboard.as_view()),
    path('instructors-requests/', InstructorsRequestsList.as_view()),
    path('accept-instructor-request/<int:pk>/', InstructorsRequestsList.as_view()),
    path('reject-instructor-request/<int:pk>/', InstructorsRequestsList.as_view()),
    path('instructors/update/', InstructorList.as_view()),
    path('rate-instructor/<int:pk>/', RateInstructor.as_view()),
    path('listing-requests/', ListingRequests.as_view()),
    path('handle-listing/<int:pk>/', HandleListingRequest.as_view()),
]