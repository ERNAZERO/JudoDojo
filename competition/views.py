from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from .serializers import StudentsInCompetitionSerializer, CompetitionSerializer
from rest_framework.views import APIView
from user.permissions import IsCoachPermission
from user.models import Student
from .models import Competition, StudentsForCompetition
from rest_framework.response import Response
from django.core.cache import cache


class CreateCompetitionView(APIView):
    permission_classes = [IsCoachPermission]

    def post(self, request):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            competition = Competition.objects.create(
                title=request.data["title"],
                competition_description=request.data["competition_description"],
                competition_date=request.data["competition_date"],
            )
            competition.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeeCompetitionsListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Попытайтесь получить данные из кэша
        cached_data = cache.get("competitions_list")

        if cached_data is not None:
            # Если данные найдены в кэше, верните их
            return Response(data=cached_data, status=status.HTTP_200_OK)
        else:
            # Если данных нет в кэше, выполните запрос к базе данных
            competitions = Competition.objects.all()
            serializer = CompetitionSerializer(competitions, many=True)

            # Сохраните данные в кэше на определенное время (например, 3600 секунд)
            cache.set("competitions_list", serializer.data, timeout=3600)

            # Верните данные клиенту
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class CompetitionDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        competition = get_object_or_404(Competition, id=id)
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # student = get_object_or_404(Student, id=id)
        # user = self.request.user
        #
        # if user.is_authenticated and user.is_Coach:
        #     serializer = StudentFullSerializer(student)
        # else:
        #     serializer = StudentLimitedSerializer(student)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class AddStudentsToCompetitionView(APIView):
    permission_classes = [IsCoachPermission]

    def post(self, request, competition_id, student_id):
        try:
            competition = Competition.objects.get(id=competition_id)
            student = Student.objects.get(id=student_id)
        except Competition.DoesNotExist:
            return Response({"message": "Competition not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        if StudentsForCompetition.objects.filter(competition=competition, student=student).exists():
            return Response({"message": "Student already in the competition"}, status=status.HTTP_400_BAD_REQUEST)
        student_for_competition = StudentsForCompetition(competition=competition, student=student)
        student_for_competition.save()
        return Response({"message": "Student was added!"}, status=status.HTTP_201_CREATED)


class SeeStudentInCompetitions(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, competition_id):
        try:
            competition = Competition.objects.get(id=competition_id)
        except Competition.DoesNotExist:
            return Response({"message": "Competition not found"}, status=status.HTTP_404_NOT_FOUND)
        students = StudentsForCompetition.objects.filter(competition=competition)
        serializer = StudentsInCompetitionSerializer(students, many=True)
        competition_serializer = CompetitionSerializer(competition)
        response_data = {
            "competition": competition_serializer.data,
            "students": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
