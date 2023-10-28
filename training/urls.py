from django.urls import path
from .views import (CreateTrainingView,
                    TrainingListView,
                    WriteStudentAttendanceView,
                    SeeStudentAttendanceView,
                    DeleteTrainingView)

urlpatterns = [
    path("create_training/", CreateTrainingView.as_view(), name="create-training"),
    path("training_list/", TrainingListView.as_view(), name="training-list"),
    path("<int:training_id>/student/<int:student_id>/write_attendance/", WriteStudentAttendanceView.as_view(), name="write-student-attendance"),
    path("student_attendances/", SeeStudentAttendanceView.as_view(), name="see-attendance"),
    path("delete_training/<int:id>", DeleteTrainingView.as_view(), name="delete-training")
]