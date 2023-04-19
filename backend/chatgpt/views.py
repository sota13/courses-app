from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from django.conf import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY




class General(APIView):
    """
    Ask generla question 
    """

    def post(self, request):
        data = request.data
        question = data.get('question')
        try:
            openai.api_key = OPENAI_API_KEY
            res = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=question,
                    max_tokens=100,
                    temperature=0
                    )
            return Response(res, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Sorry something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        
class Code(APIView):
    """
    Ask generla question 
    """

    def post(self, request):
        data = request.data
        try:
            openai.api_key = OPENAI_API_KEY
            res = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Say this is a test",
                    max_tokens=100,
                    temperature=0
                    )
            return Response(res, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Sorry something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

