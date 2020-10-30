from django import forms

from .models import ContactTeacher, Feedback, Teacher


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'feedback')


class ContactTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(Teacher.objects.all())
    name = forms.CharField()
    email = forms.EmailField()
    question = forms.CharField(widget=forms.Textarea)
