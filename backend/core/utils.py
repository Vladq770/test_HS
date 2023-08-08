import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from jwt import encode


load_dotenv()

JWT_SECRET_KEY1 = os.getenv('JWT_SECRET_KEY1')
JWT_SECRET_KEY2 = os.getenv('JWT_SECRET_KEY2')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def get_tokens(number):
    tokens = {
        'access_token': encode({'number': number}, f'{JWT_SECRET_KEY1}{int(datetime.utcnow().timestamp())}', algorithm=JWT_ALGORITHM),
        'refresh_token': encode({'number': number}, f'{JWT_SECRET_KEY2}{int(datetime.utcnow().timestamp())}', algorithm=JWT_ALGORITHM)
    }
    return tokens


def get_invite_code():
    return str(uuid.uuid4())[0:6]


def get_code():
    #return str(uuid.uuid4())[0:4]
    return '1111'

