from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_Coach = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class Belt(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.color


class Coach(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    name_of_academy = models.CharField(max_length=255, null=False, blank=False)
    dan = models.IntegerField(null=False)


class Student(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    parent_name = models.CharField(max_length=255, null=False, blank=False)
    parent_surname = models.CharField(max_length=255, null=False, blank=False)
    parent_phone_number = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    rating_points = models.IntegerField(default=0)
    belt_status = models.ForeignKey(Belt, on_delete=models.CASCADE, default=1)
    absence_day = models.IntegerField(default=0)
    injury_day = models.IntegerField(default=0)
    presence = models.IntegerField(default=0)
    avatar = models.CharField(max_length=500, blank=True, null=True)

class Group(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    group_name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    coach_id = models.ForeignKey(Coach, on_delete=models.CASCADE)


class GroupsAndStudents(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)




