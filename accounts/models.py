from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import BooleanField, CharField, DateTimeField, EmailField
from constant.string import *
# Create your models here.

class MyAccountManage(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError(create_not_email)
        if not username:
            raise ValueError(create_not_username)
        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email       = self.normalize_email(email),
            username    = username,
            password    = password,
            first_name  = first_name,
            last_name   = last_name,
        )
        user.is_active  = True
        user.is_staff   = True
        user.is_admin   = True
        user.is_superadmin  = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name  = CharField(max_length=500)
    last_name   = CharField(max_length=500)
    username    = CharField(max_length=500, unique=True)
    email       = EmailField(max_length=500, unique=True)
    phone_number= CharField(max_length=20)

    #required
    date_joined = DateTimeField(auto_now_add=True)
    last_login  = DateTimeField(auto_now_add=True)
    is_active   = BooleanField(default=True)
    is_staff    = BooleanField(default=False)
    is_admin    = BooleanField(default=False)
    is_superadmin   = BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManage()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True