from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import TestGroup, Test, Question, Answer


# Контроллер главной страницы
def index(request):
    test_groups = TestGroup.objects.all()
    context = {'test_groups': test_groups}
    return render(request, 'main/index.html', context)


# Контроллер страницы со списком тестов
def test_list(request, test_group_id):
    selected_group = TestGroup.objects.get(pk=test_group_id)
    tests = Test.objects.filter(test_group=selected_group)
    context = {'tests': tests, 'selected_group': selected_group}
    return render(request, 'main/test_list.html', context)


# Страница теста
def test_page(request, test_group_id, test_id):
    if request.method == 'GET':
        # Получаем выбранную группу и выбранный тест и добавляем их в контекст
        selected_group = TestGroup.objects.get(pk=test_group_id)
        selected_test = Test.objects.get(pk=test_id)
        context = {'selected_group': selected_group, 'selected_test': selected_test}

        # Получаем список вопросов и добавляем их в контекст
        def get_type_for_aswers_set(answers_set):
            count_correct_answer = 0
            for answer in answers_set:
                if answer.is_correct:
                    count_correct_answer += 1
            if count_correct_answer == 1:
                return 'single_type'
            else:
                return 'multiple_type'

        questions = []
        for question in Question.objects.filter(test=selected_test):
            block = {'title': question, 'answers': []}
            answers = Answer.objects.filter(question=question)
            type_for_answers = get_type_for_aswers_set(answers)
            for answer in answers:
                if type_for_answers == 'multiple_type':
                    block['answers'].append(
                        '<input type="checkbox" name="box_' + str(answer.pk) + '" value="box_' + str(
                            answer.pk) + '">' + answer.title)
                if type_for_answers == 'single_type':
                    block['answers'].append(
                        '<input type="radio" name="rad_' + str(question.pk) + '" value="rad_' + str(
                            answer.pk) + '">' + answer.title)
            questions.append(block)
        context['questions'] = questions

        return render(request, 'main/test_page.html', context)
    if request.method == 'POST':
        for p in request.POST:
            print(p, ' == ', request.POST[p])
        return HttpResponseRedirect(reverse('main:index'))
