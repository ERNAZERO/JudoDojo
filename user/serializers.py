from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Coach, Student, MyUser, Group, GroupsAndStudents


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['is_Coach'] = user.is_Coach

        #test
        token['is_staff'] = user.is_staff
        return token


class CoachSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Coach.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Coach
        fields = [
            'email',
            'name',
            'second_name',
            'phone_number',
            'description',
            'name_of_academy',
            'dan',
            'password',
            'password2',
        ]

        # {
        #             "email": "erkinkadyrakhunov@gmail.com",
        #             "name": "Erkin",
        #             "second_name": "Kadyrakhunov",
        #             "phone_number": "996707010801",
        #             "description": "Professional Judo Coach with high-level experience.",
        #             "name_of_academy":  "International Judo Academy",
        #             "dan": "5",
        #             "password": "nazka123",
        #             "password2": "nazka123"
        #         }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields did not match.'}
           )
        return attrs


class StudentFullSerializer(serializers.ModelSerializer):
    belt_status = serializers.StringRelatedField(source='belt_status.color')

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Student.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )


    class Meta:
        model =Student
        fields = [
            'id',
            'email',
            'name',
            'second_name',
            'phone_number',
            'parent_name',
            'parent_surname',
            'parent_phone_number',
            "address",
            "belt_status",
            'password',
            'password2',
            'avatar'
        ]

        # {
        #     "email": "erkinbekovernaz@gmail.com",
        #     "name": "Ernaz",
        #     "second_name": "Erkinbekov",
        #     "phone_number": "996700790296",
        #     "parent_name": "Erkin",
        #     "parent_surname": "Kadyrakhunov",
        #     "parent_phone_number": "996707010801",
        #     "address": "Micro-district kok-dzhar, 2/37",
        #     "password": "Judo2003",
        #     "password2": "Judo2003"
        # }


class StudentLimitedSerializer(serializers.ModelSerializer):
    belt_status = serializers.StringRelatedField(source='belt_status.color')
    class Meta:
        model = Student
        fields = ['id', 'name', 'second_name', 'rating_points', 'belt_status', 'avatar']


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name']


class AddStudentToGroupSerilizer(serializers.ModelSerializer):
    class Meta:
        model = GroupsAndStudents
        fields = '__all__'

# {
#     "email": "test1gmail.com",
#     "name": "test.",
#     "second_name": "TESTOV.",
#     "phone_number": "This field is required.",
#     "parent_name": "This field is required.",
#     "parent_surname": "This field is required.",
#     "parent_phone_number":"This field is required.",
#     "address": "This field is required.",
#     "password": "lalka123",
#     "password2": "lalka123"
# # }


class MyUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email']


class StudentProfileSerializer(serializers.Serializer):
    student_info = StudentFullSerializer(source='student', read_only=True)
    user_info = MyUserProfileSerializer(source='myuser', read_only=True)