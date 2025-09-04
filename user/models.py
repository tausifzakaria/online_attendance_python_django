from django.db import models
from django.contrib.auth.models import User

class studentInfo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10)
    course = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.get_full_name} ({self.student_id})"


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    start_time = models.TimeField(auto_now=False)
    end_time = models.TimeField(auto_now=False, null=True, blank = True)
