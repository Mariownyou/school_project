from django import forms

from .models import ContactTeacher, Feedback, Teacher


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'feedback')


class ContactTeacherForm(forms.ModelForm):
    class Meta:
        model = ContactTeacher
        fields = ('teacher', 'name', 'email', 'question')