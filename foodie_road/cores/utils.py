import re, jwt

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.http  import JsonResponse

from users.models      import User
from foodie_road.settings import SECRET, ALGORITHM


regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
regex_password = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~!@#$%^&*()+|=]{8,}$'

class Validation:
    def email_validate(value):
        if not re.match(regex_email,value):
            raise ValidationError('not in email format')
    def password_validate(value):
        if not re.match(regex_password,value):
            raise ValidationError('not in password format')
        
def jwt_generator(user_id):
    payload = {'user_id' : user_id, 'exp' : datetime.utcnow()+ timedelta(hours=1)}
    encoded = jwt.encode(payload, SECRET, algorithm = ALGORITHM)
    return encoded

def jwt_decoder(token):
    try: 
        decoded = jwt.decode(token, SECRET, algorithms = ALGORITHM)
        return decoded
    except  :
        raise KeyError
    
def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get("Authorization", None)
            request.user = User.objects.get(id=jwt_decoder(token)['user_id'])
            request.payload = jwt_decoder(token)
            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'IVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'signin time expired'})
    return wrapper
