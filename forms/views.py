from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail

from .forms import ContactTeacherForm, FeedbackForm
from .models import ContactTeacher, Feedback, Teacher

# Create your views here.
def send_feedback(request):
    form = FeedbackForm(request.POST or None)
    feedbacks = Feedback.objects.filter(is_approved=True)

    if form.is_valid():
        form.save()
        return redirect('index', permanent=True)
    context = {
        'form': form,
        'feedbacks': feedbacks
    }
    return render(request, 'feedback_form.html', context)


def contact_teacher(request):
    form = ContactTeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        teacher = form.cleaned_data.get("teacher")
        question = form.cleaned_data.get("question")
        teacher_email = Teacher.objects.get(name=teacher)
        send_mail(
            question, email,
            email,
            [teacher_email]
        )
        return redirect('index', permanent=True)

    context = {
        'form': form,
    }
    return render(request, 'contact_form.html', context)
