import base64
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import AnnonPermission, IsCoachPermission, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import (CoachSerializer,
                          MyTokenObtainPairSerializer,
                          StudentFullSerializer,
                          StudentLimitedSerializer,
                          CreateGroupSerializer, StudentProfileSerializer
                          )
from .models import Coach, Student, Group, GroupsAndStudents, Belt
from rest_framework import generics


def get_object(id: int, table):
    try:
        return table.objects.get(id=id)
    except table.DoesNotExist:
        raise Http404


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = self.request.user
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CoachRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            coach = Coach.objects.create(
                email=request.data['email'],
                is_Coach=True,
                is_active=True,
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                description=request.data['description'],
                name_of_academy=request.data['name_of_academy'],
                dan=request.data['dan']
            )
            coach.set_password(request.data['password'])
            coach.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StudentFullSerializer(data=request.data)
        if serializer.is_valid():
            avatar = request.data.get('avatar')
            if avatar:
                image_data = base64.b64encode(avatar.read()).decode("utf-8")
            else:
                image_data = None
            student = Student.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                is_active=True,
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                parent_name=request.data['parent_name'],
                parent_surname=request.data['parent_surname'],
                parent_phone_number=request.data['parent_phone_number'],
                address=request.data['address'],
                avatar=image_data
            )
            student.set_password(request.data['password'])
            student.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = (AnnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class StudentListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = self.request.user
        students = cache.get("student_list")

        if not students:
            students = Student.objects.all()
            if user.is_authenticated and user.is_Coach:
                serializer = StudentFullSerializer(students, many=True)
                cache.set("student_list", serializer.data, timeout=3600)
            else:
                serializer = StudentLimitedSerializer(students, many=True)
                cache.set("student_list", serializer.data, timeout=3600)

        return Response(students, status=status.HTTP_200_OK)


class StudentDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        user = self.request.user

        if user.is_authenticated and user.is_Coach:
            serializer = StudentFullSerializer(student)
        else:
            serializer = StudentLimitedSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateGroupView(APIView):
    permission_classes = [IsCoachPermission]

    def post(self, request):
        serializer = CreateGroupSerializer(data=request.data)
        coach = Coach.objects.get(id=self.request.user.id)
        if serializer.is_valid():
            group = Group.objects.create(
                group_name=request.data['group_name'],
                coach_id=coach
            )
            group.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AddStudentToGroupView(APIView):
    permission_classes = [IsCoachPermission]

    def post(self, request, group_id, student_id):
        try:
            group = Group.objects.get(id=group_id)
            student = Student.objects.get(id=student_id)
        except Group.DoesNotExist:
            return Response({"message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        if GroupsAndStudents.objects.filter(group=group, student=student).exists():
            return Response({"message": "Student already in the group"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.id != group.coach_id_id:
            print(request.user.id)
            print(group.coach_id_id)
            return Response({"message": "You are not the coach of this group"}, status=status.HTTP_403_FORBIDDEN)

        group_and_student = GroupsAndStudents(group=group, student=student)
        group_and_student.save()
        return Response({"message": "Student added to the group successfully"}, status=status.HTTP_201_CREATED)


class DeleteStudentFromGroupView(APIView):
    permission_classes = [IsCoachPermission]

    def delete(self, request, group_id, student_id):
        try:
            group = Group.objects.get(id=group_id)
            student = Student.objects.get(id=student_id)
            group_and_student = GroupsAndStudents.objects.get(group=group, student=student)
        except Group.DoesNotExist:
            return Response({"message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except GroupsAndStudents.DoesNotExist:
            return Response({"message": "Student is not in the group"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id != group.coach_id_id:
            print(request.user.id)
            print(group.coach_id_id)
            return Response({"message": "You are not the coach of this group"}, status=status.HTTP_403_FORBIDDEN)

        group_and_student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeeGroupView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        groups = Group.objects.all()
        seriliazer = CreateGroupSerializer(groups, many=True)
        return Response(seriliazer.data, status=status.HTTP_200_OK)


class SeeStudentsListInGroupView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        students_in_group = GroupsAndStudents.objects.filter(group=group).select_related('student')
        student_list = [group_and_student.student for group_and_student in students_in_group]
        serializer = StudentLimitedSerializer(student_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateBeltStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        new_belt_data = request.data.get('belt', None)
        if new_belt_data:
            try:
                new_belt = Belt.objects.get(id=new_belt_data['id'])
            except Belt.DoesNotExist:
                return Response({"message": "Belt not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Belt data is required"}, status=status.HTTP_400_BAD_REQUEST)

        student.belt_status = new_belt
        student.save()
        serializer = StudentLimitedSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddRatingPointsView(APIView):
    permission_classes = [IsCoachPermission]

    def put(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        points_to_add = request.data.get("points", 0)

        if not 1 <= points_to_add <= 10:
            return Response({"message": "Invalid number of points. It should be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        student.rating_points += points_to_add
        student.save()

        return Response({"message": "Rating points added successfully"}, status=status.HTTP_200_OK)


class StudentDeleteView(APIView):
    permission_classes = [IsCoachPermission]

    def delete(self, request, id):
        user = get_object_or_404(Student, id=id)
        if user:
            user.delete()
            return Response({"User has deleted!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        if group:
            serilizer = CreateGroupSerializer(group)
            return Response(serilizer.data, status=status.HTTP_200_OK)
        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
