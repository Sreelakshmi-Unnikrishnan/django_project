from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField

class University(models.Model):
    university = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | University: " + str(self.university)
    
class Department(models.Model):
    department = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Department: " + str(self.department)

class Specialization(models.Model):
    specialization = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Specialization: " + str(self.specialization)

class Semester(models.Model):
    semester = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Semester: " + str(self.semester)

class Subject(models.Model):
    subject = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Subject: " + str(self.subject)

class Module(models.Model):
    module_no = models.IntegerField(default=1)
    module_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Module: " + str(self.module_name)

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    # phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Teacher: " + str(self.name)

class Video(models.Model):
    video = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='thumbnails')
    title = models.CharField(max_length=200)
    description = FroalaField()
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    video_part_no = models.IntegerField(default=1)
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_this_video_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Subject: " + str(self.subject) + " | Module: " + str(self.module) + " | Video Part No: " + str(self.video_part_no)

class Course(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    
    active = models.BooleanField( default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | University: " + str(self.university) + " | Department: " + str(self.department) + " | Specialization: " + str(self.specialization) + " | Semester: " + str(self.semester)


class PurchasedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    order_amount = models.CharField(max_length=25, default=700)
    order_payment_id = models.CharField(max_length=100, default='')
    isPaid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | User: " + str(self.user.username) + " | Order amount: " + str(self.order_amount)


"""
=============================================== Star rating and Comment ==============================================================
"""


class StarRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    star_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "ID: " + str(self.id) + " | User: " + str(self.user.username) + " | Star rating: " + str(self.star_rating)

class Comment(models.Model):
    comment = models.CharField(max_length=100,  default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID: " + str(self.id) + " | Comment: " + str(self.comment)
