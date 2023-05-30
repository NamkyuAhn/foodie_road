from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, email, password):
        if not name:            
            raise ValueError('must have user name')
        if not email:            
            raise ValueError('must have user email')
        if not password:            
            raise ValueError('must have user password')

        user = self.model(            
            email = self.normalize_email(email),         
            name = name,
        )

        user.set_password(password)        
        user.save(using=self._db)        
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    order = models.ManyToManyField('stores.Store', through="orders.Order", related_name='user_order')
    like = models.ManyToManyField('stores.Store', through="users.Like", related_name='user_like')
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                                   null=True, related_name='user_like')
    store = models.ForeignKey('stores.Store', on_delete=models.SET_NULL,
                                   null=True, related_name='store_like')
    
    class Meta:
        db_table = 'likes'
