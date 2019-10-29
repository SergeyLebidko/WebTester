from django.contrib import admin
from .models import TestGroup, Test, Question, Answer


class TestGroupAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']


class TestAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']


admin.site.register(TestGroup, TestGroupAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
