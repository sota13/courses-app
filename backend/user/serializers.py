from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()



class UserProfileSerializer(serializers.ModelSerializer):
    instructor_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id','first_name', 'last_name', 'is_instructor', 'instructor_id', 'bio', 'phone_number', 'gender', 'avatar']

    def get_instructor_id(self, obj):
        if obj.is_instructor:
            return obj.user.instructor.id

        return None



class EditProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id','first_name', 'last_name', 'bio', 'avatar', 'phone_number', 'gender']



    def get_avatar(self, obj):
        return obj.get_avatar_url

    def get_phone_number(self, obj):
        return obj.phone_number

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        bio = data.get('bio','')
        phone_number = data.get('phone_number','')
        gender = data.get('gender','')
        avatar = data.get('avatar', '')
        instance.first_name = first_name
        instance.last_name = last_name
        instance.bio = bio
        instance.gender = gender
        if avatar:
            instance.avatar = avatar
        if phone_number:
            instance.phone_number = phone_number
        instance.save()
        return instance

