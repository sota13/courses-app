from rest_framework import serializers
from .models import (Instructor,
InstructorRequest, 
InstructorReview, 
InstructorEducation,
InstructorContactInfo,
InstructorSkill,
InstructorSocialMedia,
SocialMediaItem,
ContactItem,
ListingRequest
)
from user.serializers import UserProfileSerializer
from authentication.serializers import UserSerializerWithToken
from utils.mail import Sender
from utils.custom_excepiton import AllreadyExist
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from course.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()


# this is helper function to create contact and social media item for new instructors
def create_contacts_socials(ins, con_list, soc_list):
    for cn in con_list:
        InstructorContactInfo.objects.get_or_create(contact_item=cn, instructor=ins)
    for sc in soc_list:
        InstructorSocialMedia.objects.get_or_create(social_item=sc, instructor=ins)






class CourseListSerializer(serializers.ModelSerializer):
    num_enrolled = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'type', 'level', 'rating', 'num_reviews', 'language', 'num_lectures', 'num_enrolled', 'duration', 
                  'price', 'discount', 'discount_enabled', 'active', 'status', 'thumbnail', 'created_date']

    def get_num_enrolled(self, obj):
        return obj.enrollments.count()




class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorEducation
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorSkill
        fields = '__all__'


class ContactInfoSerializer(serializers.ModelSerializer):
    contact_item = serializers.StringRelatedField()
    class Meta:
        model = InstructorContactInfo
        fields = ['id', 'contact_item', 'detail', 'show']


class SocialMediaSerializer(serializers.ModelSerializer):
    social_item = serializers.StringRelatedField()

    class Meta:
        model = InstructorSocialMedia
        fields = ['id', 'social_item', 'link', 'show']


class InstructorListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(required=False, read_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = Instructor
        fields = ['id', 'specialty', 'job_title', 'approved', 'user_id', 'email', 'rating','num_reviews', 'profile']

    def get_user_id(self, obj):
        return obj.user.id

    def get_email(self, obj):
        return obj.user.email

class ShortInstructorSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(required=False, read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'approved', 'bio', 'user_id', 'email', 'phone_number', 'specialty', 'rating', 'avatar', 'listing_status']

    def get_user_id(self, obj):
        return obj.user.id

    def get_avatar(self, obj):
        return obj.profile.get_avatar_url

    def get_bio(self, obj):
        return obj.profile.bio

    def get_email(self, obj):
        return obj.user.email

    def get_phone_number(self, obj):
        return obj.profile.phone_number

    


class InstructorRegisterSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(required=False, read_only=True)
    profile = UserProfileSerializer(required=False)
    updated_user = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'user_id', 'email', 'profile', 'updated_user']

    def get_user_id(self, obj):
        return obj.user.id

    def get_email(self, obj):
        return obj.user.email

    def get_updated_user(self, obj):
        return UserSerializerWithToken(obj.user).data

    def create(self, validated_data):
        user = self.context.get('user')
        data = validated_data.pop('data')
        phone_number = data['phone_number']
        bio = data['bio']

        if user.is_anonymous:
            email = data['email']
            password = data['password']
            filtered_user_by_email = User.objects.filter(email=email)
            if filtered_user_by_email.exists():
                exist_user = auth.authenticate(email=email, password=password)
                if not exist_user:
                    raise AuthenticationFailed('Invalid credentials, try again')
                if exist_user.userprofile.is_instructor:
                    raise AllreadyExist('Allready registerd.')
                else:
                    exist_user.userprofile.phone_number = phone_number
                    exist_user.userprofile.bio = bio
                    exist_user.userprofile.is_instructor = True
                    exist_user.save()
                    new_instructor = Instructor()
                    new_instructor.user = exist_user
                    new_instructor.save()
                    contact_items = ContactItem.objects.all()
                    social_media_items = SocialMediaItem.objects.all()
                    create_contacts_socials(new_instructor, contact_items, social_media_items)
                
            else:
                new_user = User.objects.create(
                email=email,
                password=make_password(data['password']),
                )
                new_user.save()
                new_user.userprofile.phone_number = phone_number
                new_user.userprofile.bio = bio
                new_user.userprofile.is_instructor = True
                new_user.save()
                new_instructor = Instructor()
                new_instructor.user = new_user
                new_instructor.save()
                contact_items = ContactItem.objects.all()
                social_media_items = SocialMediaItem.objects.all()
                create_contacts_socials(new_instructor, contact_items, social_media_items)
        else:
            if user.userprofile.is_instructor:
                    raise AllreadyExist('Allready registerd.')
            user.userprofile.phone_number = phone_number
            user.userprofile.bio = bio
            user.userprofile.is_instructor = True
            user.save()
            new_instructor = Instructor()
            new_instructor.user = user
            new_instructor.save()
            contact_items = ContactItem.objects.all()
            social_media_items = SocialMediaItem.objects.all()
            create_contacts_socials(new_instructor, contact_items, social_media_items)

        instructor_request = InstructorRequest()
        instructor_request.instructor = new_instructor
        instructor_request.save()
        email_data = {
            'content': "new instructor request to register as an instructor", 
            'to': "mohad.sota@gmail.com",
            'subject': 'new instructor'}
        Sender.send_email(email_data)
        return new_instructor

    def update(self, instance, validated_data):
        user = self.context.get('user')
        data = validated_data.pop('data')
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        gender = data['gender']
        bio = data['bio']
        avatar = data.get('avatar', '')
        user.first_name = first_name
        user.last_name = last_name
        user.profile.phone_number = phone_number
        user.profile.gender = gender
        user.profile.bio = bio
        user.is_instructor = True
        if avatar:
            user.profile.avatar = avatar
        user.save()


        #here I'm going to convert the json array to python list, since form data can't send normal array

        # instance.sections_teaching.clear()
        # sections_teaching = data['sections_teaching']
        # asections_teaching = json.loads(sections_teaching)
        # print(sections_teaching)
        # for section in asections_teaching:
        #     section = Section.objects.get(id=section['id'])
        #     instance.sections_teaching.add(section)

       

        instance.save()
        return instance

class ShortListingSerializer(serializers.ModelSerializer):
    request_date = serializers.SerializerMethodField()

    class Meta:
        model = ListingRequest
        fields = ['id', 'is_seen', 'is_handled', 'instructor_message','reviewer_decision', 'reviewer_note', 'request_date', 'request_type', 'terms_accepted']
    
    def get_request_date(self, obj):
        return obj.request_date.strftime("%d/%m/%Y")
    
class InstructorProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    # sections_teaching = SectionListSerializer(many=True)
    courses = serializers.SerializerMethodField(read_only=True)
    # contributed_courses = LightCourseSerializer(many=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    reviewers_ids = serializers.SerializerMethodField(read_only=True)
    education = EducationSerializer(many=True)
    skills = SkillSerializer(many=True)
    contact_info = ContactInfoSerializer(many=True)
    social_media = SocialMediaSerializer(many=True)


    class Meta:
        model = Instructor
        fields = ['id', 'user_id', 'email', 'first_name', 'last_name', 'reviewers_ids',
                  'phone_number', 'gender', 'bio', 'rating', 'num_reviews', 'courses',
                   'specialty', 'avatar', 'reviews', 'education', 'skills', 'contact_info', 'social_media',
                  ]

    def get_user_id(self, obj):
        return obj.user.id

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.profile.first_name

    def get_last_name(self, obj):
        return obj.profile.last_name

    def get_phone_number(self, obj):
        return obj.profile.phone_number

    def get_gender(self, obj):
        return obj.profile.gender


    def get_bio(self, obj):
        return obj.profile.bio

    def get_avatar(self, obj):
        return obj.profile.get_avatar_url

    def get_courses(self, obj):
        courses = obj.courses.filter(active=True)
        serializer = CourseListSerializer(courses, many=True)
        return serializer.data

    

    def get_reviews(self, obj):
        reviews = obj.instructorreview_set.all()
        serializer = InstructorReviewSerializer(reviews, many=True)
        return serializer.data

    def get_reviewers_ids(self, obj):
        reviews = obj.instructorreview_set.all()
        reviewers_ids = [x.reviewer.id for x in reviews]
        return reviewers_ids


class InstructorDashboardSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    # sections_teaching = SectionListSerializer(many=True)
    courses = serializers.SerializerMethodField(read_only=True)
    # contributed_courses = LightCourseSerializer(many=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    reviewers_ids = serializers.SerializerMethodField(read_only=True)
    education = EducationSerializer(many=True)
    skills = SkillSerializer(many=True)
    contact_info = ContactInfoSerializer(many=True)
    social_media = SocialMediaSerializer(many=True)
    listing_requests = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Instructor
        fields = ['id', 'approved', 'listing_status', 'user_id', 'email', 'first_name', 'last_name', 'reviewers_ids',
                  'phone_number', 'gender', 'bio', 'rating', 'num_reviews',
                   'specialty', 'job_title', 'avatar', 'courses', 'reviews', 'education', 'skills', 'contact_info', 'social_media',
                   'listing_requests',
                  ]

    def get_user_id(self, obj):
        return obj.user.id

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.profile.first_name

    def get_last_name(self, obj):
        return obj.profile.last_name

    def get_phone_number(self, obj):
        return obj.profile.phone_number

    def get_gender(self, obj):
        return obj.profile.gender


    def get_bio(self, obj):
        return obj.profile.bio

    def get_avatar(self, obj):
        return obj.profile.get_avatar_url

    def get_courses(self, obj):
        courses = obj.courses.filter(active=True)
        serializer = CourseListSerializer(courses, many=True)
        return serializer.data
    
    def get_listing_requests(self, obj):
        listing_requests = obj.listing_requests.filter(is_handled=True)
        serializer = ShortListingSerializer(listing_requests, many=True)
        return serializer.data

    

    def get_reviews(self, obj):
        reviews = obj.instructorreview_set.all()
        serializer = InstructorReviewSerializer(reviews, many=True)
        return serializer.data

    def get_reviewers_ids(self, obj):
        reviews = obj.instructorreview_set.all()
        reviewers_ids = [x.reviewer.id for x in reviews]
        return reviewers_ids


class InstructorsRequestsSerializer(serializers.ModelSerializer):
    instructor = ShortInstructorSerializer()

    class Meta:
        model = InstructorRequest
        fields = ['id', 'instructor', 'requested_date', 'is_seen']


class InstructorReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InstructorReview
        fields = ['id','reviewer_name', 'rating', 'comment', 'created_date']

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.userprofile.first_name} {obj.reviewer.userprofile.last_name}"



class InstructorGeneralInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'specialty', 'job_title', 'first_name', 'last_name', 'bio', 'avatar']

    def get_first_name(self, obj):
        return obj.profile.first_name

    def get_last_name(self, obj):
        return obj.profile.last_name

    def get_bio(self, obj):
        return obj.profile.bio

    def get_avatar(self, obj):
        return obj.profile.get_avatar_url

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        specialty = data.get('specialty')
        job_title = data.get('job_title')
        bio = data.get('bio','')
        avatar = data.get('avatar', '')
        instance.profile.first_name = first_name
        instance.profile.last_name = last_name
        instance.profile.bio = bio
        if avatar:
            instance.profile.avatar = avatar
        instance.profile.save()

        instance.specialty = specialty
        instance.job_title = job_title
        instance.save()
        return instance


class InstructorQualificationsSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    skills = SkillSerializer(many=True)
    
    class Meta:
        model = Instructor
        fields = ['id','education', 'skills']


    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        education = data.get('education')
        skills = data.get('skills')

        instance.education.clear()
        for ed in education:
            educationItem = InstructorEducation.objects.create(institution=ed['institution'], detail=ed['detail'], instructor=instance)

        instance.skills.clear()
        for sk in skills:
            sklillItem = InstructorSkill.objects.create(name=sk['name'], level=sk['level'], instructor=instance)
        
        instance.save()
        return instance


class InstructorContactSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Instructor
        fields = ['id','contact_info']


    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        contact_info = data.get('contact_info')

        for cn in contact_info:
            contact_item, created = ContactItem.objects.get_or_create(name=cn['contact_item'])
            contactItem, created = InstructorContactInfo.objects.get_or_create(contact_item=contact_item, instructor=instance)
            contactItem.detail = cn['detail']
            contactItem.show = cn['show']
            contactItem.save()
        
        instance.save()
        return instance


class InstructorSocialSerializer(serializers.ModelSerializer):
    social_media = SocialMediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Instructor
        fields = ['id','social_media']


    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        social_media = data.get('social_media')

        for sc in social_media:
            social_item, created = SocialMediaItem.objects.get_or_create(name=sc['social_item'])
            ins_social_item, created = InstructorSocialMedia.objects.get_or_create(social_item=social_item, instructor=instance)
            ins_social_item.link = sc['link']
            ins_social_item.show = sc['show']
            ins_social_item.save()
        
        instance.save()

        
        return instance

class InstructorPasswordSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField()
    
    class Meta:
        model = Instructor
        fields = ['id','password']

    def get_password(self, obj):
        return obj.user.password


    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        user = instance.user
        new_password = data.get('new_password','')
        

        user.password = make_password(new_password)
        user.save()
                

        
        return instance

class ListingSerializer(serializers.ModelSerializer):
    instructor = ShortInstructorSerializer(read_only=True)
    request_date = serializers.SerializerMethodField()

    class Meta:
        model = ListingRequest
        fields = ['id', 'instructor', 'is_seen', 'is_handled', 'instructor_message','reviewer_decision', 'reviewer_note', 'request_date', 'request_type', 'terms_accepted']
    
    def get_request_date(self, obj):
        return obj.request_date.strftime("%d/%m/%Y")
    
    def create(self, validated_data):
        user = self.context.get('user')
        instructor = user.instructor
        data = validated_data.pop('data')
        request_type = data.get('request_type')
        instructor_message = data.get('instructor_message')

        list_req = ListingRequest()
        list_req.request_type = request_type
        list_req.instructor_message = instructor_message
        list_req.instructor = instructor
        if request_type == 'list':
            list_req.terms_accepted = data.get('terms_accepted')
            instructor.listing_status = "pending"
            instructor.save()
        elif request_type == 'unlist':
            list_req.is_handled = True 
            instructor.listing_status = "unlisted"
            instructor.save()

        list_req.save()

        

        return list_req


class HandleListingSerializer(serializers.ModelSerializer):
    instructor = ShortInstructorSerializer(read_only=True)
    request_date = serializers.SerializerMethodField()

    class Meta:
        model = ListingRequest
        fields = ['id', 'instructor', 'is_seen', 'is_handled', 'instructor_message','reviewer_decision', 'reviewer_note', 'request_date', 'request_type', 'terms_accepted']

    def get_request_date(self, obj):
        return obj.request_date.strftime("%d/%m/%Y")

    def update(self, instance, validated_data):
        user = self.context.get('user')
        data = validated_data.pop('data')
        decision = data.get('decision')
        reviewer_note = data.get('reviewer_note')
        new_status = 'listed' if decision == 'list' else "unlisted"



        instance.reviewer_note = reviewer_note
        instance.reviewer = user
        instance.reviewer_decision = decision
        instance.is_handled = True
        instance.is_seen = True
        instance.save()

        instructor = instance.instructor
        instructor.listing_status = new_status
        instructor.save()

        return instance

        
