from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Chapter, Course, Section, Lecture, CourseReview, CartItem, LectureStatus, PublicationRequest, EnrolledCourse
from .serializers import (CreateSectionSerializer, SectionCoursesSerializer, SectionListSerializer,
                          CourseListSerializer,
                          CourseChaptersSerializer,
                          ChapterSerializer,
                          LightCourseSerializer,
                          CourseDetailSerializer,
                          LectureSerializer,
                          CourseReviewSerializer,
                          CreateCourseSerializer,
                          CourseDashboardSerializer,
                          BenefitSerializer,
                          FaqSerializer,
                          UpdateCourseInfoSerializer,
                          UpdateCourseDescription,
                          UpdateCourseFaqs,
                          UpdateCourseImage,
                          UpdateCoursePublication,
                          HandleCoursePublication,
                          CoursePriceSerializer,
                          CartItemSerializer,
                          CoursePageSerializer,
                          UserCoursesSerializer,
                          PublicationSerializer,
                          EnrolledCoursesSerializer
                          )
from instructor.serializers import InstructorListSerializer
import boto3
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class SectionList(APIView):
    """
    List all sections, or create a new Section.
    """

    def get(self, request):
        sections = Section.objects.all()
        serializer = SectionListSerializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionCourses(APIView):
    """
    List all  courses for a spesific section
    """

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        section = self.get_object(pk)
        serializer = SectionCoursesSerializer(section)
        return Response(serializer.data)


class CourseList(APIView):
    """
    List all  courses, or create a new course.
    """

    def get(self, request):
        # courses = Course.objects.filter(active=True,status='published')
        courses = Course.objects.filter(status='published')
        serializer = CourseListSerializer(courses, many=True)
        return Response( {"courses_list": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateCourseSerializer(data=request.data, context={
            'user': request.user})
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserCourses(APIView):
    """
    List all user courses
    """

    def get(self, request):
        user = request.user
        enrolled_courses = user.enrolled_courses.all()
        serializer = EnrolledCoursesSerializer(enrolled_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetail(APIView):
    """
    Get, Update or Delete a course.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        course = self.get_object(pk)
        course.active = False
        course.save()
        return Response(pk)



class CoursePage(APIView):
    """
    Get course page.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CoursePageSerializer(course, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseDashboard(APIView):
    """
    Get, Update or Delete a course in dashboard section.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseDashboardSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        print(request.data)
        course = self.get_object(pk)
        part = request.data.get('part')
        if part == 'course_info':
            serializer = UpdateCourseInfoSerializer(instance=course, data=request.data)
        elif part == 'description':
            serializer = UpdateCourseDescription(instance=course, data=request.data)
        elif part == 'faqs':
            serializer = UpdateCourseFaqs(instance=course, data=request.data)
        elif part == 'image':
            serializer = UpdateCourseImage(instance=course, data=request.data)
        elif part == 'publication':
            serializer = UpdateCoursePublication(instance=course, data=request.data, context={'user': request.user})
        
        else:
            return Response({"issue":"you should provide which part you want to update"}, status=status.HTTP_200_OK)

        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.active = False
        course.save()
        return Response(pk)

class PublicationRequests(APIView):
    """
    List all publications requests, or create a new Section.
    """

    def get(self, request):
        publications_requests = PublicationRequest.objects.filter(is_handled=False)
        serializer = PublicationSerializer(publications_requests, many=True)
        return Response(serializer.data)


class HandlePublication(APIView):
    """
    handle publication requests.
    """
    def get_object(self, pk):
        try:
            return PublicationRequest.objects.get(id=pk)
        except PublicationRequest.DoesNotExist:
            raise Http404


    def patch(self, request, pk):
        pub_req = self.get_object(pk)
        serializer = HandleCoursePublication(instance=pub_req, data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCourse(APIView):
    """
    Retrieve, update or delete  user courses.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request):
        user = request.user
        courses = user.courses.all()
        enrollment_request = user.enrollment_requests.all()
        serializer = LightCourseSerializer(
            courses, many=True)
        courses_ids = [course.id for course in courses]
        requested_courses_ids = [req.course.id for req in enrollment_request]
        user_courses_details = {
            "courses":serializer.data,
            "courses_ids": {
            "user_courses_ids":courses_ids,
            "requested_courses_ids":requested_courses_ids
            }
        }
        return Response({user_courses_details})

    def delete(self, request, pk):
        user = request.user
        course = self.get_object(pk)
        user.courses.remove(course)
        message = {'course_id': pk, 'text': 'course deleted successfuly!'}
        return Response(message)


class CourseChapters(APIView):
    """
    List all course's chapters.
    """
    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        owner_id = course.instructor.user.id
        instructor_approved = course.instructor.approved
        course_name = course.name
        course_method = course.method
        print(course_name)
        chapters = course.chapters.all()
        serializer = CourseChaptersSerializer(
            chapters, many=True, context={'user': request.user})
        course_chapters = serializer.data
        data = {
            "owner_id": owner_id,
            "instructor_approved": instructor_approved,
            "course_name":course_name,
            "course_ID":course.id,
            "course_method":course_method,
            "status":course.status,
            "chapters": course_chapters
        }
        return Response(data, status=status.HTTP_200_OK)


class CourseEnroll(APIView):
    """
    enroll users to courses.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        course = self.get_object(pk)
        if course.type =='free':
            EnrolledCourse.objects.create(user=request.user, course=course, method='free')
            serializer = LightCourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message':'sorry somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class CoursePrice(APIView):
    """
    price detail for a course.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CoursePriceSerializer(course)
        return Response(serializer.data)

class CartItems(APIView):
    """
    Add Course Item.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        course = self.get_object(pk)
        cart_item = CartItem.objects.create(course=course, user=request.user)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        cart_item = CartItem.objects.get(id=pk)
        cart_item.delete()
        return Response(pk)

class ChapterList(APIView):
    """
    List all chapters, or create a new chapter.
    """

    def get(self, request):
        chapters = Chapter.objects.all()
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseChaptersSerializer(data=request.data, context={
            'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChapterDetail(APIView):
    """
    Update and deleta chapters.
    """
    def get_object(self, pk):
        try:
            return Chapter.objects.get(id=pk)
        except Chapter.DoesNotExist:
            raise Http404


    def patch(self, request, pk):
        chapter = self.get_object(pk)
        serializer = CourseChaptersSerializer(
            chapter, data=request.data)
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        chapter = self.get_object(pk)
        lectures = chapter.lectures.all()
        bucket_name=settings.AWS_STORAGE_BUCKET_NAME
        s3 = boto3.resource('s3')
        if lectures:
            for lec in lectures:
                key = lec.key
                s3.Object(bucket_name, key).delete()
                lec.delete()

        chapter.delete()
        return Response(pk)

class CreateCourseBenefit(APIView):
    """
    create a new course benefits.
    """

    def post(self, request):
        serializer = BenefitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateCourseFaq(APIView):
    """
    create a new course faq.
    """

    def post(self, request):
        serializer = FaqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionInstructors(APIView):
    """
    List all section's instructors'.
    """

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))
        dist = offset+limit
        section = self.get_object(pk)
        instructors = section.instructors.all()[offset:dist]
        serializer = InstructorListSerializer(instructors, many=True)
        return Response(serializer.data)


class UploadLecture(APIView):
    """
    upload lectures.
    """

    def post(self, request):
        user = request.user
        serializer = LectureSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save(data=request.data)
            lecture_details = {
                "chapterId":request.data.get('chapter_id'),
                "uploadedLecture":serializer.data
            }
            return Response(lecture_details, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LectureDetail(APIView):
    def get_object(self, pk):
        try:
            return Lecture.objects.get(id=pk)
        except Lecture.DoesNotExist:
            raise Http404


    def patch(self, request, pk):
        lecture = self.get_object(pk)
        serializer = LectureSerializer(
            lecture, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lecture = self.get_object(pk)
        chapter_id = lecture.chapter.id
        key = lecture.key
        bucket_name=settings.AWS_STORAGE_BUCKET_NAME
        hls_key = lecture.formatted_vid_key
        s3 = boto3.resource('s3')
        if key:
            s3.Object(bucket_name, key).delete()
        if hls_key:
            hls_bucket = s3.Bucket(lecture.formatted_vid_bucket) 
            hls_bucket.objects.filter(Prefix=hls_key+"/").delete()
        lecture.delete()
        return Response({"lectureId":pk, "chapterId":chapter_id})



class PublishCourse(APIView):
    """
    publish a course and make it available in courses store
    """
    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        course = self.get_object(pk)
        course.status = 'published'
        course.save()
        print('course will be puplished')
        data = {
            "status":course.status
        }
        return Response(data=data, status=status.HTTP_200_OK)

    
class UnPublishCourse(APIView):
    """
    unpublish a course and make it  not available in courses store
    """
    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        course = self.get_object(pk)
        course.status = 'unpublished'
        course.save()
        print('course will be unpuplished')
        data = {
            "status":course.status
        }
        return Response(data=data, status=status.HTTP_200_OK)

class FrontendUpload(APIView):
    """
    genereta a presigned url to upload file and write the instance details
    """
    def post(self, request):
        data=request.data
        print(data)
        try:
            s3Client = boto3.client("s3", region_name="me-south-1",endpoint_url="https://s3.me-south-1.amazonaws.com")
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)
        
        
        bucketName = data.get('bucket_name')
        fileKey = data.get('file_key')
        expiryTime = data.get('expiry_time')
        action = data.get('action')
            
        try:
            print(bucketName)
            URL = s3Client.generate_presigned_url(
                "put_object" if action =="upload" else "get_object",
                Params = {"Bucket":bucketName, "Key":fileKey},
                ExpiresIn = expiryTime
                )
            return Response({"url":URL}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)


class RateCourse(APIView):
    """
    create a review and rate course.
    """

    def get_object(self, pk):
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        reviewer = request.user
        course = self.get_object(pk)
        data = request.data

        # 1 - Review already exists
        alreadyExists = course.reviews.filter(reviewer=reviewer).exists()
        if alreadyExists:
            content = {'detail': 'Course already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2 - No Rating or 0
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3 - Create review
        else:
            review = CourseReview.objects.create(
                reviewer=reviewer,
                course=course,
                rating=data['rating'],
                comment=data['comment'],
            )

            # this is the old way of calculating the course rating and number of review, but it seems to be so expensive, so I change it
            # reviews = course.coursereview_set.all()
            # course.num_reviews = len(reviews)

            # total = 0
            # for i in reviews:
            #     total += i.rating

            # course.rating = total / len(reviews)

            # this my new approach of calculating the course rating and number of review
            old_num_reviews = course.num_reviews
            new_num_reviews = old_num_reviews + 1
            new_total_rating = course.total_rating + int(data.get('rating'))
            course.total_rating = new_total_rating
            course.num_reviews = new_num_reviews
            course.rating = new_total_rating / new_num_reviews

            course.save()
            serializerd_review = CourseReviewSerializer(review).data

            return Response(serializerd_review, status=status.HTTP_200_OK)


class MarkCompletedLecture(APIView):
    """
    Mark Lecture as completed.
    """

    def get_object(self, pk):
        try:
            return Lecture.objects.get(id=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        lecture = self.get_object(pk)
        user = request.user
        lecture_status, created = LectureStatus.objects.get_or_create(
            lecture=lecture, user=user)
        if (lecture_status.is_completed is False):
            lecture_status.is_completed = True
            lecture_status.save()
        serializer = LectureSerializer(lecture, context={'user': user})
        return Response(serializer.data)