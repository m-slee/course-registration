from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=4)
    course_name = models.CharField(max_length=100)
    course_prefix = models.CharField(max_length=3)
    subject = models.CharField(max_length=32)
    course_open = models.BooleanField(default=True)
    capicty = models.IntegerField()
    description = models.CharField(max_length=255)
    teacher = models.CharField(max_length=30)
    enrollee = models.ManyToManyField(User, related_name="student", blank=True) # make migrations to update blank=True

    def __str__(self):
        return f"{self.course_prefix} - {self.course_id}: {self.course_name}"

# the enrollees is just using the built in User model,
# so three tables are being represented with one here,
# counting the many-to-many created by migrations