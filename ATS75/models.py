from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    student=models.OneToOneField(User,on_delete=models.CASCADE)
    student_institution=models.CharField(max_length=100)
    schedule_start_date=models.DateField(null=True,blank=True)
    schedule_end_date=models.DateField(null=True,blank=True)
    threshold=models.FloatField(null=True,blank=True)

    def __str__(self):
        return str(self.student.username)+" : "+str(self.student_institution) # pylint: disable=no-member


class Subject(models.Model):
    subject_code=models.CharField(max_length=10)
    subject_name=models.CharField(max_length=50)
    teacher_name=models.CharField(max_length=50)

    # user_ref: to know who owns this subject
    user_ref=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        unique_together=(("user_ref","subject_code"),)

    def __str__(self):
        return str(self.user_ref.student.username)+" : "+str(self.subject_code)+':'+str(self.subject_name) #pylint: disable=no-member



class TTCell(models.Model):
    #Row of TT
    day=models.CharField(max_length=3)
    #Column of TT
    time_slot_start=models.TimeField()
    time_slot_end=models.TimeField()
    #value
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)

    # user_ref: to know who owns this cell as we are making TT with cells that points to user
    user_ref=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        unique_together=(("user_ref","day","time_slot_start"),)

    def __str__(self):
        return str(self.user_ref.student.username)+" : "+str(self.day)+" : "+str(self.time_slot_start)+"-"+str(self.time_slot_end) #pylint:disable=no-member



class ARCell(models.Model):
    #Row of Attendence Record
    date=models.DateField()
    #Column of Attendence Record
    time_slot_start=models.TimeField()
    time_slot_end=models.TimeField()
    #value
    value=models.CharField(max_length=2)

    #user_ref:
    user_ref=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        unique_together=(("user_ref","date","time_slot_start"),)

    def __str__(self):
        return str(self.user_ref.student.username)+" : "+str(self.date)+" : "+str(self.time_slot_start)+"-"+str(self.time_slot_end) #pylint:disable=no-member