from django.contrib import admin
from .models import TestGroup, Test, Question, Answer


# Встроенные редакторы
class TestInline(admin.StackedInline):
    model = Test
    extra = 0


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


# Блок редакторов моделей
class TestGroupAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    search_fields = ['title']
    inlines = [TestInline]


class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_group']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['test_group']
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'test']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['test']
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['title', 'question']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['question']


admin.site.register(TestGroup, TestGroupAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
