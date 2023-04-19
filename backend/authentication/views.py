from .serializers import MyTokenSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, UserSerializer, UserSerializerWithToken, ActionLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from utils.mail import Sender
from course.models import Course, CartItem
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginView(APIView):
    """
    login a user.
    """
    def post(self, request):
        serializer = MyTokenSerializer(data=request.data)
        try:
            serializer.is_valid()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e.args)
            message = {'message': 'somehing went wrong, pleace check your credencial', 'detail':e.args}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class ActionLoginView(APIView):
    """
    login a user.
    """
    def post(self, request):
        serializer = ActionLoginSerializer(data=request.data)
        serializer.is_valid()
        try:
            serializer.is_valid()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except:
            message = {'message': 'somehing went wrong, pleace check your credencial'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(APIView):
    """
    create a new user.
    """

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                email=data['email'],
                password=make_password(data['password']),
            )
            user.userprofile.first_name = data['first_name']
            user.userprofile.last_name = data['last_name']
            user.save()

            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            message = {'message': 'somehing went wrong, pleace check your credencial', 'detail': e.args}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class ActionRegisterUser(APIView):
    """
    create a new user.
    """

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                email=data['email'],
                password=make_password(data['password']),
            )
            user.userprofile.first_name = data['first_name']
            user.userprofile.last_name = data['last_name']
            user.save()

            course_id = data.get('course_id')
            action_type = data.get('action_type')
            if course_id and action_type:
                if action_type == 'enroll':
                    user.courses.add(course_id)
                    user.save()
                elif action_type == 'cart':
                    course = Course.objects.get(id=course_id)
                    CartItem.objects.create(course=course, user=user)
                    user.save()

            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            message = {'message': 'somehing went wrong, pleace check your credencial', 'detail': e.args}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """
    List all users.
    """

    #permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            #absurl = 'http://'+current_site + relativeLink
            absurl = settings.BACKEND_URL + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Reset your passsword'}
            # Util.send_email(data)
            data = {'content': email_body, 'to': user.email,
                    'subject': 'Reset your passsword'}
            Sender.send_email(data)
            
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = ['http', 'https']


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(settings.FRONTEND_URL+'/?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(settings.FRONTEND_URL+redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(f'{settings.FRONTEND_URL}/xxx'+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



class RequestVerifyEmail(APIView):

    def get(self,request):
        user = request.user
        token = RefreshToken.for_user(user).access_token
        relativeLink = reverse('verify-email')
        redirect_url = request.GET.get('redirect_url', '')
        absurl = settings.BACKEND_URL + relativeLink + "?token="+str(token)+"&redirect_url="+redirect_url
        email_body = 'Hello, \n Use the link below to verify your email  \n' + \
            absurl
        
        data = {'content': email_body, 'to': user.email,
                    'subject': 'Verify Email'}
        
        Sender.send_email(data)

        return Response({'email': 'Activating email has sent successfully'}, status=status.HTTP_200_OK)

class VerifyEmail(APIView):


    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        redirect_url = request.GET.get('redirect_url', '')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            if redirect_url:
                return CustomRedirect(settings.FRONTEND_URL+redirect_url)
            
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)