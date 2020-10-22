from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
        return redirect('index', permanent=True)

    context = {
        'form': form,
    }
    return render(request, 'contact_form.html', context)
