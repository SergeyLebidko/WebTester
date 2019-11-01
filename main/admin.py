from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import TestGroup, Test, Question, Answer


# Класс, который будет осуществлять валидацию набора ответов, связанных с каким-либо вопросом
class AnswerFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        # Количество ответов
        count_answers = 0

        # Количество правильных ответов
        count_correct_answers = 0

        for form in self.forms:
            form_data = form.cleaned_data
            if not form_data['DELETE']:
                count_answers += 1
            if form_data['is_correct']:
                count_correct_answers += 1

        if not (0 < count_correct_answers < count_answers):
            raise ValidationError('Количество вариантов ответов должно быть больше двух и должен'
                                  ' существовать хотя бы один правильный ответ')


# Встроенный редактор для добавления ответов
class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    formset = AnswerFormSet


# Фильтр для корректного отображения списка тестов в зависимости от выбранной группы тестов
class TestFilter(admin.SimpleListFilter):
    title = 'Название теста'
    parameter_name = 'test'

    def lookups(self, request, model_admin):
        # Получаем выбранную пользователем группу и возвращаем перечень тестов, входящих в эту группу
        if 'test__test_group__id__exact' in request.GET:
            group_id = request.GET['test__test_group__id__exact']
            selected_group = TestGroup.objects.get(pk=group_id)
            return ((test.pk, test.title) for test in Test.objects.filter(test_group=selected_group))
        else:
            # Если пользователь не выбрал ни одну группу, возвращаем перечень всех тестов, которые есть в системе
            return ((test.pk, test.title) for test in Test.objects.all())

    def queryset(self, request, queryset):
        test_id = self.value()
        if test_id is None:
            return queryset

        selected_test = Test.objects.get(pk=test_id)
        return queryset.filter(test=selected_test)


# Редакторы моделей
class TestGroupAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    search_fields = ['title']


class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_group']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = [
        ('test_group', admin.RelatedOnlyFieldListFilter)
    ]
    autocomplete_fields = ('test_group',)

    # Данный метод переопределен, чтобы при добавлении нового теста поле группы было заполнено автоматически
    def get_changeform_initial_data(self, request):
        if '_changelist_filters' in request.GET:
            line = request.GET['_changelist_filters']
            group_id = int(line.split('=')[1])
            selected_group = TestGroup.objects.get(pk=group_id)
            return {'test_group': selected_group}
        return super().get_changeform_initial_data(request)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'test']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = [
        'test__test_group',
        TestFilter
    ]
    inlines = [AnswerInline]
    autocomplete_fields = ('test',)

    # Данный метод переопределен, чтобы при вводе нового вопроса не нужно было выбирать тест,
    # если он предварительно отобран в фильтре
    def get_changeform_initial_data(self, request):
        if '_changelist_filters' in request.GET:
            line = request.GET['_changelist_filters']
            params = {}
            for s in line.split('&'):
                params[s.split('=')[0]] = s.split('=')[1]
            if 'test' in params:
                test_id = int(params['test'])
                selected_test = Test.objects.get(pk=test_id)
                return {'test': selected_test}
        return super().get_changeform_initial_data(request)


admin.site.register(TestGroup, TestGroupAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
