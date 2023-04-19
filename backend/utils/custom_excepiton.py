from rest_framework.exceptions import APIException
from rest_framework import status


class AllreadyExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Allready Exist"
    default_code = "Allready Exist"

class WrongPassword(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "WrongPassword"
    default_code = "WrongPassword"