from django.db import models
from user.models import Student


class Competition(models.Model):
    title = models.CharField(max_length=255, null=False)
    competition_description = models.CharField(max_length=500, null=False)
    competition_date = models.DateTimeField(null=False)


class StudentsForCompetition(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


