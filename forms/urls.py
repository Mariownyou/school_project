from django.urls import path

from . import views

urlpatterns = [
    path('feedback', views.send_feedback, name='feedback'),
    path('contact_teacher', views.contact_teacher, name='contact_teacher'),
]