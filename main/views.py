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
            postfix = 0
            for answer in answers:
                if type_for_answers == 'multiple_type':
                    block['answers'].append(
                        '<input type="checkbox" name="' + str(question.pk) + '_' + str(postfix) + '" value="' + str(
                            answer.pk) + '">' + answer.title)
                    postfix += 1
                if type_for_answers == 'single_type':
                    block['answers'].append(
                        '<input type="radio" name="' + str(question.pk) + '" value="' + str(
                            answer.pk) + '">' + answer.title)
            questions.append(block)
        context['questions'] = questions

        return render(request, 'main/test_page.html', context)
    if request.method == 'POST':
        # Формируем словарь с ответами пользователя
        user_answers = {}

        for param in request.POST:
            if not param.startswith('csrf'):
                question_id = param.split('_')[0]
                if question_id not in user_answers:
                    user_answers[question_id] = []
                user_answers[question_id].append(request.POST[param])

        # Формируем словарь с правильными ответами
        correct_answers = {}
        selected_test = Test.objects.get(pk=test_id)
        questions = Question.objects.filter(test=selected_test)

        for question in questions:
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                if answer.is_correct:
                    if str(question.pk) not in correct_answers:
                        correct_answers[str(question.pk)] = []
                    correct_answers[str(question.pk)].append(str(answer.pk))

        # Если пользователь ответил не на все вопросы - переводим ему на страницу с соответствующим сообщением
        if len(user_answers) != len(correct_answers):
            return render(request, 'main/invalid_answer_count.html',
                          {'test_group_id': test_group_id, 'test_id': test_id})

        # Сверяем ответы
        # Количество неправильных ответов
        incorrect_answer_count = 0
        correct_answer_count = 0
        for question_id in correct_answers:
            if correct_answers[question_id] == user_answers[question_id]:
                correct_answer_count += 1
            else:
                incorrect_answer_count += 1

        # Формируем контекст
        context = {
            'correct_answer_count': correct_answer_count,
            'incorrect_answer_count': incorrect_answer_count,
            'test_group_id': test_group_id,
            'test_id': test_id
        }

        # Переводим пользователя на страницу статистики
        return render(request, 'main/test_statistic.html', context)
