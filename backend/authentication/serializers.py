from django.contrib.auth.models import update_last_login
from rest_framework.serializers import ModelSerializer, CharField ,SerializerMethodField, Serializer, EmailField, IntegerField, StringRelatedField
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserProfileSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from course.models import Course, CartItem
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class PasswordField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)


# this serializer was made to avoid circular import, since I can't imported from course serilizers
class CoursePriceSerializer(ModelSerializer):
    instructor = StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'thumbnail', 'price',  'discount', 'discount_enabled',
                  'instructor']

# this serializer was made to avoid circular import, since I can't imported from course serilizers
class CartItemSerializer(ModelSerializer):
    course = CoursePriceSerializer()
    

    class Meta:
        model = CartItem
        fields = ['id', 'course']




class UserSerializer(ModelSerializer):
    profile = SerializerMethodField(read_only=True)
    name = SerializerMethodField(read_only=True)
    enrolled_courses = SerializerMethodField(read_only=True)
    cart_items = CartItemSerializer(many=True)
    cart_courses_ids = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'is_admin', 'profile', 'enrolled_courses', 'cart_items', 'cart_courses_ids']

    def get_name(self, obj):
        return f"{obj.userprofile.first_name} {obj.userprofile.last_name}"

    def get_profile(self, obj):
        return UserProfileSerializer(obj.userprofile).data

    def get_enrolled_courses(self, obj):
        return [en.course.id for en in obj.enrolled_courses.all()] 

    def get_cart_courses_ids(self, obj):
        return [it.course.id for it in obj.cart_items.all()] 


class UserSerializerWithToken(ModelSerializer):
    token = SerializerMethodField(read_only=True)
    profile = SerializerMethodField(read_only=True)
    name = SerializerMethodField(read_only=True)
    enrolled_courses = SerializerMethodField(read_only=True)
    cart_items = CartItemSerializer(many=True)
    cart_courses_ids = SerializerMethodField(read_only=True)
    

    class Meta:
        model = User
        fields = ['id','email', 'name', 'is_admin', 'profile', 'enrolled_courses', 'token', 'cart_items', 'cart_courses_ids']

    def get_name(self, obj):
        if not obj.userprofile.first_name or not obj.userprofile.last_name:
            return 'nameles user'
        return f"{obj.userprofile.first_name} {obj.userprofile.last_name}"

    def get_profile(self, obj):
        return UserProfileSerializer(obj.userprofile).data

    def get_enrolled_courses(self, obj):
        return [en.course.id for en in obj.enrolled_courses.all()] 

    def get_cart_courses_ids(self, obj):
        return [it.course.id for it in obj.cart_items.all()] 

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class MyTokenSerializer(Serializer):
    username_field = get_user_model().USERNAME_FIELD
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)

        # Add custom claims
        #token['first_name'] = user.first_name
        #token['last_name'] = user.last_name
        # ...

        return token

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = CharField()
        self.fields["password"] = PasswordField()
        

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        refresh = self.get_token(self.user)

        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        data = {}

        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v

        data['token'] = token

        update_last_login(None, self.user)

        return data

class ActionLoginSerializer(Serializer):
    username_field = get_user_model().USERNAME_FIELD
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)

        # Add custom claims
        #token['first_name'] = user.first_name
        #token['last_name'] = user.last_name
        # ...

        return token

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = CharField()
        self.fields["password"] = PasswordField()
        self.fields["course_id"] = IntegerField()
        self.fields["action_type"] = CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        refresh = self.get_token(self.user)

        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        data = {}

        print(attrs)

        course_id = attrs["course_id"]
        action_type = attrs["action_type"]
        if course_id and action_type:
            if action_type == 'enroll':
                self.user.courses.add(course_id)
                self.user.save()
            elif action_type == 'cart':
                course = Course.objects.get(id=course_id)
                if not CartItem.objects.filter(course=course, user=self.user).exists():
                    CartItem.objects.create(course=course, user=self.user)
                    self.user.save()
        

        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v

        data['token'] = token

        update_last_login(None, self.user)

        return data

        
class ResetPasswordEmailRequestSerializer(Serializer):
    email = EmailField(min_length=2)

    redirect_url = CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(Serializer):
    password = CharField(
        min_length=6, max_length=68, write_only=True)
    token = CharField(
        min_length=1, write_only=True)
    uidb64 = CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

