import json

from users.models import User, Like
from stores.models import Store, StoreImage
from cores.utils import jwt_generator, signin_decorator, Validation

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db.utils            import IntegrityError
from django.core.exceptions     import ValidationError
from django.contrib.auth        import authenticate

class SignupView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            name      = data['name']
            email     = data['email']
            password  = data['password']

            Validation.email_validate(email)
            Validation.password_validate(password)
            
            User.objects.create_user(
                name      = name,
                password  = password,
                email     = email,
            )

            return JsonResponse({'message' : 'signup success'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status = 400)

        except IntegrityError:
            return JsonResponse({'message' : 'email is already exists'}, status = 400)

        except ValueError as e:
            return JsonResponse({'message' : f'{e}'}, status = 400)

        except ValidationError as e:
            e = str(e)[2:-2]
            return JsonResponse({'message' : f'{e}'}, status = 400)

class EmailUniqueCheckView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            if not User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'email unique check pass'}, status = 200)
            return JsonResponse({'message' : 'email already exists'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status = 400)

class SigninView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']

        user = authenticate(email=email, password=password)

        if user is not None:              
            return JsonResponse({'message' : 'signin success', 'token' : jwt_generator(user.id)}, status = 200)
            
        else:
            return JsonResponse({'message' : 'check email or password'}, status = 400)
        
class LikeView(View):
    @signin_decorator
    def get(self,request):
        try : 
            likes = Like.objects.filter(user_id = request.user.id)
            result = []
            for like in likes:
                store = Store.objects.get(id = like.store_id)
                store_image = StoreImage.objects.get(store_id = store.id)
                result.append({
                        "store_id" : store.id,
                        "store_name" : store.store_name,
                        "store_thumnail" : store_image.image_urls
                    })
            return JsonResponse({'likes' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status = 400) 
    
    @signin_decorator
    def post(self,request):
        try :
            data = json.loads(request.body)
            store_id = data['store_id']

            Like.objects.create(  
                user_id = request.user.id,
                store_id = store_id,
            )
            return JsonResponse({'message' : 'like created'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status = 400)