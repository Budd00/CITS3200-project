from django.db import models
import uuid

# Create your models here.
class membership(models.Model):
    member_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    student_number = models.IntegerField
    is_committee = models.BooleanField(default=False)
    exception = models.BooleanField(default=False)
    join_date = models.DateField
    expire_date = models.DateField


class member_exception(models.Model):
    notes = models.CharField(max_length=100)
    exception_date = models.DateField
