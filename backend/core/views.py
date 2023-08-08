from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *


@api_view(['POST'])
def get_code(request):
    res, code = get_code_service(request.data)
    return Response(res, code)


@api_view(['POST'])
def check_code(request):
    res, code = check_code_service(request.data)
    return Response(res, code)


@api_view(['POST'])
def get_profile(request):
    res, code = get_profile_service(request.data)
    return Response(res, code)


@api_view(['POST'])
def enter_invite(request):
    res, code = enter_invite_service(request.data)
    return Response(res, code)


@api_view(['POST'])
def refresh_tokens(request):
    res, code = refresh_tokens_service(request.data)
    return Response(res, code)
