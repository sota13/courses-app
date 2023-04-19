from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EditProfileSerializer
from django.contrib.auth.hashers import make_password



class EditProfile(APIView):
    """
    Update user profile.
    """

    def patch(self, request):
        user = request.user
        serializer = EditProfileSerializer(user.userprofile, data=request.data)
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserPassword(APIView):
    """
    Update user password.
    """

    def patch(self, request):
        user = request.user
        if user.check_password(request.data.get('current_password')):
            new_password = request.data.get('new_password','')
            user.password = make_password(new_password)
            user.save()
            return Response({'message':'password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'make sure to write the current password correctly'}, status=status.HTTP_400_BAD_REQUEST)






