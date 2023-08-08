import os
import redis
from dotenv import load_dotenv
from copy import copy
from django.utils import timezone
from django.db import transaction, IntegrityError
from .tasks import send_code_task
from .models import User
from .utils import *
from .serializers import UserSerializer, UserSerializerSimple


load_dotenv()

bad_code = {'mes': 'Incorrect code'}
code_sent = {'mes': 'Code sent'}
bad_token = {'mes': 'Token is not found'}
bad_invite = {'mes': 'Invite code not found'}
already_referral = {'mes': 'The user is already a referral'}
success = {'mes': 'Successfully!'}
bad_referrer = {'mes': 'This user cant be your referrer'}

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

expiration_time_access = int(os.getenv('EXPIRATION_TIME_ACCESS'))
expiration_time_refresh = int(os.getenv('EXPIRATION_TIME_REFRESH'))

redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))


def check_token(number, token):
    if f'{number}access' in redis_instance and token == (redis_instance.get(f'{number}access')).decode('utf-8'):
        return True
    return False


def get_code_service(data):
    code = get_code()
    number = data['phone_number']
    if not User.objects.filter(phone_number=number).first():
        invite_code = get_invite_code()
        while(User.objects.filter(invite_code=invite_code).first()):
            invite_code = get_invite_code()
        User.objects.create(phone_number=number, invite_code=invite_code)
        user = User.objects.get(phone_number=number)
        user.username = f'user{user.id}'
        user.save()
    redis_instance.set(f'{number}_code', code, expiration_time_access)
    send_code_task.delay(number, code)
    return code_sent, 200


def check_code_service(data):
    number = data['phone_number']
    code = data['code']
    if f'{number}_code' in redis_instance and code == (redis_instance.get(f'{number}_code')).decode('utf-8'):
        redis_instance.delete(f'{number}_code')
        user = User.objects.get(phone_number=number)
        tokens = get_tokens(number)
        redis_instance.set(f'{number}access', tokens['access_token'], expiration_time_access)
        redis_instance.set(f'{number}refresh', tokens['refresh_token'], expiration_time_refresh)
        refs = UserSerializerSimple(user.refs.all(), many=True).data
        user = UserSerializer(user).data
        user['tokens'] = tokens
        user['refs'] = refs
        return user, 200
    return bad_code, 400


def get_profile_service(data):
    token = data['access_token']
    number = data['phone_number']
    if not check_token(number, token):
        return bad_token, 400
    user = User.objects.get(phone_number=number)
    refs = UserSerializerSimple(user.refs.all(), many=True).data
    user = UserSerializer(user).data
    user['refs'] = refs
    return user, 200


def enter_invite_service(data):
    token = data['access_token']
    number = data['phone_number']
    invite_code = data['invite_code']
    if not check_token(number, token):
        return bad_token, 400
    user = User.objects.get(phone_number=number)
    if user.is_ref:
        return already_referral, 400
    if referrer := User.objects.filter(invite_code=invite_code).first():
        if referrer in user.refs.all():
            return bad_referrer, 200
        with transaction.atomic():
            user.referrer = referrer
            user.is_ref = True
            user.save()
        return success, 200
    return bad_invite, 400


def refresh_tokens_service(data):
    token = data['refresh_token']
    number = data['phone_number']
    if f'{number}refresh' in redis_instance and token == (redis_instance.get(f'{number}refresh')).decode("utf-8"):
        tokens = get_tokens(number)
        redis_instance.set(f'{number}access', tokens['access_token'], expiration_time_access)
        redis_instance.set(f'{number}refresh', tokens['refresh_token'], expiration_time_refresh)
        return tokens, 200
    return bad_token, 400



