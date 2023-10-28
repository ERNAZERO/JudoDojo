from .models import Competition, StudentsForCompetition
from rest_framework import serializers
from user.serializers import StudentLimitedSerializer

class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition
        fields = "__all__"


# class StudentsInCompetitionSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = StudentsForCompetition
#         fields = "__all__"


class StudentsInCompetitionSerializer(serializers.ModelSerializer):

    student = StudentLimitedSerializer()  # Сериализатор для студента

    class Meta:
        model = StudentsForCompetition
        fields = ["student"]