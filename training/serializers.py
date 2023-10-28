from .models import Training, StudentAttendance
from rest_framework import serializers


class TrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = ["title", "description", "training_date", "group"]
        # fields = "__all__"


class StudentAttendanceSerializer(serializers.ModelSerializer):
    # student = serializers.StringRelatedField(source='student.name')
    class Meta:
        model = StudentAttendance
        fields = "__all__"



