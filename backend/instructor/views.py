from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from instructor.models import Instructor, InstructorRequest, InstructorReview, ListingRequest
from instructor.serializers import (
    InstructorListSerializer,
    InstructorProfileSerializer, 
    InstructorRegisterSerializer, 
    InstructorReviewSerializer, 
    InstructorsRequestsSerializer,
    InstructorGeneralInfoSerializer,
    InstructorQualificationsSerializer,
    InstructorContactSerializer,
    InstructorSocialSerializer,
    InstructorPasswordSerializer,
    InstructorDashboardSerializer,
    ListingSerializer,
    HandleListingSerializer
)
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()




class InstructorList(APIView):
    """
    List all instructors, register new an instrutor, and update instructor profile
    """

    def get(self, request):
        instructors = Instructor.objects.filter(approved=True, listing_status='listed')
        serializer = InstructorListSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InstructorRegisterSerializer(
            data=request.data, context={'user': request.user})
        print(request.user.is_anonymous)
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        instructor = request.user.instructor
        serializer = InstructorRegisterSerializer(
            instance=instructor, data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstructorProfile(APIView):
    """
    Retrieve, update or delete an insructor.
    """

    def get_object(self, pk):
        try:
            return Instructor.objects.get(id=pk)
        except Instructor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # user = User.objects.get(id=pk)
        # instructor = user.instructor
        instructor = self.get_object(pk)
        serializer = InstructorProfileSerializer(instructor)
        return Response(serializer.data)



class InstructorDashboard(APIView):
    """
    Retrieve, update or delete an insructor.
    """

    def get_object(self, pk):
        try:
            return Instructor.objects.get(id=pk)
        except Instructor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instructor = self.get_object(pk)
        serializer = InstructorDashboardSerializer(instructor)
        return Response(serializer.data)

    def put(self, request, pk):
        instructor = self.get_object(pk)
        serializer = InstructorDashboardSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        instructor = self.get_object(pk)
        part = request.data.get('part')
        
        if part == 'general_info':
            serializer = InstructorGeneralInfoSerializer(instructor, data=request.data)
        elif part == 'qualifications':
            serializer = InstructorQualificationsSerializer(instructor, data=request.data)
        elif part == 'contact_info':
            serializer = InstructorContactSerializer(instructor, data=request.data)
        elif part == 'social_media':
            serializer = InstructorSocialSerializer(instructor, data=request.data)
        elif part == 'password':
            # serializer = InstructorPasswordSerializer(instructor, data=request.data)
            if instructor.user.check_password(request.data.get('current_password')):
                serializer = InstructorPasswordSerializer(instructor, data=request.data)
            else:
                return Response({'detail':'make sure to write the current password correctly'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail':'something went wrong pleace tell the admin'}, status=status.HTTP_400_BAD_REQUEST)

            


        if serializer.is_valid(raise_exception=True):
            serializer.save(data=request.data)
            updatedInstructor = InstructorDashboardSerializer(instructor).data
            return Response(updatedInstructor, status=status.HTTP_200_OK)
        return Response({'detail':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instructor = self.get_object(pk)
        instructor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class InstructorsRequestsList(APIView):
    """
    Retrieve, accept, or deny instructors requests to become an instructor.
    """

    def get_object(self, pk):
        try:
            return InstructorRequest.objects.get(id=pk)
        except InstructorRequest.DoesNotExist:
            raise Http404

    def get(self, request):
        requests = InstructorRequest.objects.filter(is_handled=False)
        for req in requests:
            if req.is_seen == False:
                req.is_seen = True
                req.save()
        serializer = InstructorsRequestsSerializer(
            requests, many=True)
        return Response(serializer.data)

    # this function for accepting request
    def post(self, request, pk):
        instructor_request = self.get_object(pk)
        instructor = instructor_request.instructor
        instructor.approved =True
        instructor.approved_date = datetime.datetime.now()
        instructor.save()
        instructor_request.is_handled =True
        instructor_request.decision = 'approved'
        instructor_request.save()

        return Response(pk, status=status.HTTP_200_OK)

    # this function for rejecting request
    def patch(self, request, pk):
        instructor_request = self.get_object(pk)
        instructor = instructor_request.instructor
        instructor.approved = False
        instructor.save()
        instructor_request.is_handled =True
        instructor_request.decision = 'rejected'
        instructor_request.save()
        return Response(pk)




class RateInstructor(APIView):
    """
    create a review and rate instructor.
    """

    def get_object(self, pk):
        try:
            return Instructor.objects.get(id=pk)
        except Instructor.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        reviewer = request.user
        instructor = self.get_object(pk)
        data = request.data

        # 1 - Review already exists
        alreadyExists = instructor.instructorreview_set.filter(reviewer=reviewer).exists()
        if alreadyExists:
            content = {'detail': 'Insructor already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2 - No Rating or 0
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3 - Create review
        else:
            review = InstructorReview.objects.create(
                reviewer=reviewer,
                instructor=instructor,
                rating=data['rating'],
                comment=data['comment'],
            )

            reviews = instructor.instructorreview_set.all()
            num_reviews = len(reviews)
            instructor.num_reviews = num_reviews

            total = 0
            for i in reviews:
                total += i.rating

            if num_reviews:
                instructor.rating = total / num_reviews

            instructor.save()
            serializerd_review = InstructorReviewSerializer(review).data

            return Response(serializerd_review, status=status.HTTP_200_OK)



class ListingRequests(APIView):
    """
    List all listing requests.
    """

    def get(self, request):
        listing_requests = ListingRequest.objects.filter(is_handled=False)
        serializer = ListingSerializer(listing_requests, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user

        if ListingRequest.objects.filter(instructor=user.instructor, is_handled=False).exists():
            return Response({"message":"you already have a request not handled yet"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ListingSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HandleListingRequest(APIView):
    """
    handle listng requests.
    """
    def get_object(self, pk):
        try:
            return ListingRequest.objects.get(id=pk)
        except ListingRequest.DoesNotExist:
            raise Http404


    def patch(self, request, pk):
        list_req = self.get_object(pk)
        serializer = HandleListingSerializer(instance=list_req, data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

