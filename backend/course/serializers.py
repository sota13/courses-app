from rest_framework import serializers
from .models import Section, Course, Chapter, Lecture, LectureStatus, CourseReview, CourseBenefit, CourseFaq, PublicationRequest, CartItem, EnrolledCourse
from instructor.serializers import ShortInstructorSerializer
import json
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()





class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'number']


class PublicationCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'thumbnail']


class SectionListSerializer(serializers.ModelSerializer):
    num_instuctors = serializers.SerializerMethodField()
    num_courses = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'name', 'num_instuctors', 'num_courses']

    def get_num_instuctors(self, obj):
        return obj.instructors.count()
        

    def get_num_courses(self, obj):
        return obj.courses.count()
        

class CreateSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ['id', 'name']


class BenefitSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseBenefit
        fields = ['id', 'description']

class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseFaq
        fields = ['id', 'question', 'answer']

class PublicationSerializer(serializers.ModelSerializer):
    instructor = ShortInstructorSerializer()
    course = PublicationCourseSerializer()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = PublicationRequest
        fields = ['id', 'instructor', 'course', 'is_seen', 'is_handled', 'instructor_message','reviewer_decision', 'reviewer_note', 'created_date', 'request_type', 'terms_accepted']
    
    def get_created_date(self, obj):
        return obj.created_date.strftime("%d/%m/%Y")

class LectureStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = LectureStatus
        fields = ['id', 'is_completed']


class LectureSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    chapter_id = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'type', 'number', 'duration','convert_status', 'key', 'source', 'formatted_vid_url', 'cloudfront_url', 'is_completed', 'chapter_id']


    def get_chapter_id(self, obj):
        return obj.chapter.id

    def get_duration(self, obj):
        duration = obj.duration if obj.duration else 0 
        return str(timedelta(seconds=round(duration)))


    def get_is_completed(self, obj):
        user = self.context.get('user')
        if LectureStatus.objects.filter(lecture=obj, user=user).exists():
            lecture_status = LectureStatus.objects.get(lecture=obj, user=user)
            return lecture_status.is_completed
        else:
            return False


    def create(self, validated_data):
        user = self.context.get('user')
        lecture = Lecture()
        data = validated_data.pop('data')
        chapter_id = data['chapter_id']
        chapter = Chapter.objects.get(id=chapter_id)
        instructor = user.instructor
        lecture.chapter = chapter
        lecture.instructor = instructor
        lecture.title = validated_data.get('title')
        lecture.number = validated_data.get('number')
        # lecture.duration = validated_data.get('duration')
        lecture.type = validated_data.get('type')
        lecture.source = validated_data.get('source')
        lecture.key = validated_data.get('key')
        lecture.save()
        # lectures_list = chapter.lectures.all()
        # chapter.num_lectures = len(lectures_list)
        # print(len(lectures_list))
        # total_duration = 0
        # for lc in lectures_list:
        #     total_duration += lc.duration if lc.duration else 0
        # chapter.duration = total_duration
        # chapter.save()
        return lecture


class CourseChaptersSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, required=False)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'number', 'num_lectures', 'duration', 'course', 'lectures']

    def get_duration(self, obj):
        duration = obj.duration if obj.duration else 0 
        return str(timedelta(seconds=round(duration)))


    def create(self, validated_data):
        user = self.context.get('user')
        new_chapter = Chapter()
        new_chapter.name = validated_data.get('name')
        new_chapter.number = validated_data.get('number')
        new_chapter.course = validated_data.get('course')
        new_chapter.instructor = user.instructor
        new_chapter.save()
        return new_chapter





class CourseReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField(read_only=True)
    reviewer_avatar = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseReview
        fields = ['id','reviewer_name', 'reviewer_avatar', 'rating', 'comment', 'created_date']

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.userprofile.first_name} {obj.reviewer.userprofile.last_name}"

    def get_reviewer_avatar(self, obj):
        return obj.reviewer.userprofile.get_avatar_url

    def get_created_date(self, obj):
        return obj.created_date.strftime("%b %d, %Y")




class CourseListSerializer(serializers.ModelSerializer):
    sections = SectionListSerializer(many=True)
    instructor = serializers.StringRelatedField()
    # duration = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'type', 'level', 'rating', 'num_reviews', 'language', 'num_lectures', 'duration', 'sections', 'instructor', 'description',
                  'price', 'discount', 'discount_enabled', 'active', 'status', 'thumbnail', 'created_date', 'last_update']

    # def get_duration(self, obj):
    #     duration = obj.duration if obj.duration else 0 
    #     return str(timedelta(seconds=round(duration)))

class UserCoursesSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'type', 'level', 'rating', 'num_reviews', 'language', 'num_lectures', 'duration', 'instructor', 'description',
                  'price', 'discount', 'discount_enabled', 'active', 'status', 'thumbnail', 'created_date', 'last_update']
        
class EnrolledCoursesSerializer(serializers.ModelSerializer):
    course = UserCoursesSerializer()

    class Meta:
        model = EnrolledCourse
        fields = ['id', 'course', 'enrolled_date']




class CourseDetailSerializer(serializers.ModelSerializer):
    instructor = ShortInstructorSerializer()
    chapters = CourseChaptersSerializer(many=True)
    benefits = BenefitSerializer(many=True)
    faqs = FaqSerializer(many=True)
    reviews = CourseReviewSerializer(many=True)
    

    class Meta:
        model = Course
        fields = ['id', 'name',  'level', 'type','duration', 'benefits', 'faqs', 'instructor', 'description',
                  'price', 'discount', 'discount_enabled', 'thumbnail', 'chapters','reviews']


class CoursePageSerializer(serializers.ModelSerializer):
    instructor = ShortInstructorSerializer()
    chapters = CourseChaptersSerializer(many=True)
    faqs = FaqSerializer(many=True)
    reviews = CourseReviewSerializer(many=True)
    

    class Meta:
        model = Course
        fields = ['id', 'name',  'level', 'type','duration', 'faqs', 'instructor', 'description',
                  'price', 'discount', 'discount_enabled', 'thumbnail', 'chapters','rating', 'reviews']

    
    
class CreateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'level', 'type', 'language',  'instructor', 'description',
                  'price', 'discount', 'discount_enabled', 'thumbnail']

    def create(self, validated_data):
        user = self.context.get('user')
        data = validated_data.pop('data')
        print(validated_data.get('language'))
        print(data)
        new_course = Course()
        new_course.name = validated_data.get('name')
        new_course.brief = validated_data.get('brief')
        new_course.type = validated_data.get('type')
        new_course.description = validated_data.get('description')
        new_course.thumbnail = validated_data.get('thumbnail')
        new_course.price = validated_data.get('price')
        new_course.language = validated_data.get('language')
        new_course.level = validated_data.get('level')
        new_course.discount = validated_data.get('discount')
        new_course.discount_enabled = validated_data.get('discount_enabled')
        new_course.instructor = user.instructor
        new_course.save()

        #here I'm going to convert the json array to python list, since form data can't send normal array

        sections = data.get('sections',[])
        sections_list = json.loads(sections)
        print(sections)
        for section in sections_list:
            section = Section.objects.get(id=section['id'])
            new_course.sections.add(section)

        
        return new_course


class SectionCoursesSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'courses']

    


class LightCourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()
    sections = SectionListSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'sections',  'language',
                  'instructor', 'thumbnail']

class CoursePriceSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'thumbnail', 'price',  'discount', 'discount_enabled',
                  'instructor']

class CartItemSerializer(serializers.ModelSerializer):
    course = CoursePriceSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'course']




class CourseDashboardSerializer(serializers.ModelSerializer):
    sections = SectionListSerializer(many=True)
    instructor = ShortInstructorSerializer()
    chapters = CourseChaptersSerializer(many=True)
    benefits = BenefitSerializer(many=True)
    faqs = FaqSerializer(many=True)
    duration = serializers.SerializerMethodField()
    publication_requests = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'level', 'type', 'language', 'num_lectures', 'duration', 'benefits', 'faqs', 'status', 'sections', 'instructor', 'description',
                  'price', 'discount', 'discount_enabled', 'thumbnail', 'chapters', 'publication_requests']

    def get_duration(self, obj):
        duration = obj.duration if obj.duration else 0 
        return str(timedelta(seconds=round(duration)))

    def get_publication_requests(self, obj):
        requests = obj.publication_requests.filter(is_handled=True)
        return PublicationSerializer(requests, many=True).data


class UpdateCourseInfoSerializer(serializers.ModelSerializer):
    sections = SectionListSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'level', 'type', 'language', 'sections',
                  'price', 'discount', 'discount_enabled']

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        instance.name = data.get('name','')
        instance.brief = data.get('brief','')
        instance.level = data.get('level','')
        instance.type = data.get('type','')
        instance.language = data.get('language','')
        instance.price = data.get('price','')
        instance.discount = data.get('discount','')
        instance.discount_enabled = data.get('discount_enabled','')
        
        instance.sections.clear()
        sections = data.get('sections',[])
        for section in sections:
            section = Section.objects.get(id=section['id'])
            instance.sections.add(section)


        instance.save()

        return instance


class UpdateCourseDescription(serializers.ModelSerializer):
    benefits = BenefitSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'description', 'benefits']

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        instance.description = data.get('description','')
        
        
        instance.benefits.all().delete()
        benefits = data.get('benefits',[])
        for benefit in benefits:
            CourseBenefit.objects.create(description=benefit.get('description',''), course=instance)


        instance.save()

        return instance

class UpdateCourseFaqs(serializers.ModelSerializer):
    faqs = FaqSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'faqs']

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        type = data.get('type')

        if type == 'add':
            faq = data.get('faq')
            CourseFaq.objects.create(question=faq.get('question',''), answer=faq.get('answer',''), course=instance)
        elif type == 'update':
            new_faq = data.get('faq')
            faq_id = data.get('faq_id')
            faq = CourseFaq.objects.get(id=faq_id)
            faq.question=new_faq.get('question','')
            faq.answer=new_faq.get('answer','')
            faq.save()
        elif type == 'delete':
            faq_id = data.get('faq_id')
            faq = CourseFaq.objects.get(id=faq_id)
            faq.delete()
        
        
        


        instance.save()

        return instance



class UpdateCourseImage(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'thumbnail']

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        thumbnail = data.get('thumbnail')
        instance.thumbnail = thumbnail
        instance.save()
        return instance

class UpdateCoursePublication(serializers.ModelSerializer):
    publication_requests = PublicationSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'publication_requests']

    def update(self, instance, validated_data):
        user = self.context.get('user')
        data = validated_data.pop('data')
        request_type = data.get('request_type')
        instructor_message = data.get('instructor_message')

        pub_req = PublicationRequest()
        pub_req.request_type = request_type
        pub_req.instructor_message = instructor_message
        pub_req.course = instance
        pub_req.instructor = user.instructor
        if request_type == 'publish':
            pub_req.terms_accepted = data.get('terms_accepted')
        pub_req.save()

        instance.status = "pending"
        instance.save()
        return instance

class HandleCoursePublication(serializers.ModelSerializer):
    publication_requests = PublicationSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'publication_requests']

    def update(self, instance, validated_data):
        user = self.context.get('user')
        data = validated_data.pop('data')
        decision = data.get('decision')
        reviewer_note = data.get('reviewer_note')
        new_status = 'published' if decision == 'publish' else "unpublished"

        # requests = instance.publication_requests.all()

        # for req in requests:
        #     req.is_handled = True
        #     req.is_seen = True
        #     req.save()



        instance.reviewer_note = reviewer_note
        instance.reviewer = user
        instance.reviewer_decision = new_status
        instance.is_handled = True
        instance.is_seen = True
        instance.save()

        course = instance.course
        course.status = new_status
        course.save()

        return instance

        
