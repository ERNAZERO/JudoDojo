from django.db import models
from django.utils import timezone
from user.models import Group, Student


class Training(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название тренировки")
    description = models.TextField(verbose_name="Описание тренировки")
    present_count = models.PositiveIntegerField(default=0, verbose_name="Число присутствующих")
    absent_count = models.PositiveIntegerField(default=0, verbose_name="Число отсутствующих")
    injured_count = models.PositiveIntegerField(default=0, verbose_name="Число заболевших/травмированных")
    training_date = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    was_sick = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.training}"