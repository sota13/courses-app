from rest_framework import serializers
from .models import Review
from course.models import Course
from instructor.models import Instructor
from django.contrib.auth import get_user_model

User = get_user_model()



class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'level', 'rating', 'num_lectures', 'duration']


class PopularCoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'brief', 'type', 'level', 'rating', 'num_reviews', 'language', 'num_lectures', 'duration', 'description',
                  'price', 'discount', 'discount_enabled', 'active', 'status', 'thumbnail', 'created_date', 'last_update']

class InstructorListSerializer(serializers.ModelSerializer):
    bio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'bio', 'specialty']

    def get_bio(self, obj):
        return obj.profile.bio


class FeaturedInstructorSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'specialty', 'avatar']


    def get_avatar(self, obj):
        return obj.profile.get_avatar_url


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField(read_only=True)
    reviewer_avatar = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id','reviewer_name', 'reviewer_avatar', 'rating', 'comment', 'created_date']

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.userprofile.first_name} {obj.reviewer.userprofile.last_name}"

    def get_reviewer_avatar(self, obj):
        return obj.reviewer.userprofile.get_avatar_url

    def get_created_date(self, obj):
        return obj.created_date.strftime("%d/%m/%Y")




    