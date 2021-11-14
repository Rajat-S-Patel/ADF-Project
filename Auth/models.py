from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self,username,email,password,**other_fields):
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username,email,password,**other_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_created=True, default=timezone.now)
    image=models.ImageField(upload_to='profile_photos')
    
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username