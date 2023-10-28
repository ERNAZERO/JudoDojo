from .models import Training, StudentAttendance
from .serializers import TrainingSerializer, StudentAttendanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from user.permissions import IsCoachPermission
from user.models import Coach, Group, Student
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class CreateTrainingView(APIView):
    permission_classes = [IsCoachPermission]

    def post(self, request):
        serializer = TrainingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                group_id = request.data["group"]
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

            training = Training.objects.create(
                title=request.data["title"],
                description=request.data["description"],
                training_date=request.data["training_date"],
                group=group
            )
            training.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTrainingView(APIView):
    permission_classes = [IsCoachPermission]

    def delete(self, request, id):
        training = get_object_or_404(Training, id=id)
        if training:
            training.delete()
            return Response({"message": "Deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)

#
# class StudentListView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#     def get(self, request):
#         user = self.request.user
#         students = cache.get("student_list")
#
#         if not students:
#             students = Student.objects.all()
#             if user.is_authenticated and user.is_Coach:
#                 serializer = StudentFullSerializer(students, many=True)
#                 cache.set("student_list", serializer.data, timeout=3600)
#             else:
#                 serializer = StudentLimitedSerializer(students, many=True)
#                 cache.set("student_list", serializer.data, timeout=3600)
#
#         return Response(students, status=status.HTTP_200_OK)


class TrainingListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        training_data = cache.get("training_list")
        if training_data is None:
            trainings = Training.objects.all()
            serializer = TrainingSerializer(trainings, many=True)
            cache.set("training_list", serializer.data, timeout=3600)
        else:
            serializer = training_data

        return Response(data=serializer, status=status.HTTP_200_OK)



class WriteStudentAttendanceView(APIView):
    permission_classes = [IsCoachPermission]

    def post(self, request, training_id, student_id):
        attended = request.data.get('attended', False)
        was_sick = request.data.get('was_sick', False)

        try:
            training = Training.objects.get(id=training_id)
            student = Student.objects.get(id=student_id)
        except Training.DoesNotExist:
            return Response({"message": "Training not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        existing_attendance = StudentAttendance.objects.filter(training=training, student=student).first()
        if existing_attendance:
            return Response({"message": "Attendance already recorded for this student and training"},
                            status=status.HTTP_400_BAD_REQUEST)

        student_attendance = StudentAttendance.objects.create(
            student=student,
            training=training,
            attended=attended,
            was_sick=was_sick
        )
        student_attendance.save()
        return Response({"message": "Attendance recorded successfully"}, status=status.HTTP_200_OK)


class SeeStudentAttendanceView(APIView):
    permission_classes = [IsCoachPermission]

    def get(self, request):
        student_attendances = StudentAttendance.objects.all()
        serializer = StudentAttendanceSerializer(student_attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)