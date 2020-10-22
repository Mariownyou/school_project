from django.db import models


class Teacher(models.Model):
    name = models.CharField('Name', max_length=200)
    email = models.EmailField('Email')

    def __str__(self):
        name = self.name
        return name

class Feedback(models.Model):
    name = models.CharField('Name', max_length=200)
    email = models.EmailField('Email')
    feedback = models.TextField('feedback')
    is_approved = models.BooleanField(default=False)


class ContactTeacher(models.Model):
    name = models.CharField('Name', max_length=200)
    email = models.EmailField('Email')
    question = models.TextField('Question')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teachers')