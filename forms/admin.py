from django.contrib import admin

from .models import ContactTeacher, Feedback, Teacher
# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedback')
    search_fields = ('name',)


class ContactTeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'question')
    search_fields = ('name', 'teacher',)


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(ContactTeacher, ContactTeacherAdmin)
