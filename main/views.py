from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from .models import TestGroup, Test, Question, Answer, TestResult
from .forms import UserRegisterForm, UserEditForm


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
@login_required(login_url=reverse_lazy('main:login'))
def test_page(request, test_group_id, test_id):
    if request.method == 'GET':
        # Получаем выбранную группу и выбранный тест и добавляем их в контекст
        # Если получить информацию не удалось, то переводим пользователя на страницу с соответствующим сообщением
        try:
            selected_group = TestGroup.objects.get(pk=test_group_id)
            selected_test = Test.objects.get(pk=test_id)
            context = {'selected_group': selected_group, 'selected_test': selected_test}
        except (TestGroup.DoesNotExist, Test.DoesNotExist):
            return render(request, 'main/test_not_found_page.html', {})

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
        # Список вопросов, на которые были даны неверные ответы
        incorrect_questions_list = []
        for question_id in correct_answers:
            if correct_answers[question_id] == user_answers[question_id]:
                correct_answer_count += 1
            else:
                incorrect_answer_count += 1
                incorrect_questions_list.append(Question.objects.get(pk=question_id))

        # Добавляем результат пользователя в его статистику
        test_result = TestResult()
        test_result.user = request.user
        test_result.test = selected_test
        test_result.correct_count = correct_answer_count
        test_result.incorrect_count = incorrect_answer_count
        test_result.save()

        # Формируем контекст
        context = {
            'correct_answer_count': correct_answer_count,
            'incorrect_answer_count': incorrect_answer_count,
            'incorrect_questions_list': incorrect_questions_list,
            'test_group_id': test_group_id,
            'test_id': test_id
        }

        # Переводим пользователя на страницу статистики
        return render(request, 'main/test_statistic.html', context)


# Страница аккаунта
@login_required(login_url=reverse_lazy('main:login'))
def account(request):
    return render(request, 'main/account.html', {})


# Страница статистики пользователя
@login_required(login_url=reverse_lazy('main:login'))
def statistic_page(request):
    # Список пройденных тестов и их результатов
    passed_tests = []

    # Во внешнем цикле перебираем все тесты
    for test in Test.objects.all().order_by('title'):
        results = TestResult.objects.filter(test=test, user=request.user).order_by('date_test')
        if not results.exists():
            continue

        # Во внутреннем цикле перебираем все результаты теста, полученного во внешнем цикле и добавляем их в список
        passed_tests.append({'test': test, 'result_test': []})
        for result in results:
            passed_tests[-1]['result_test'].append(result)

    context = {'passed_tests': passed_tests}
    return render(request, 'main/user_satistic.html', context)


# Контроллер страницы поиска
def find_page(request):
    if request.method == 'GET':
        return render(request, 'main/find_page.html', {})
    if request.method == 'POST':
        find_text = request.POST['find_text']
        find_text = find_text.strip().lower()
        if not find_text:
            return HttpResponseRedirect(reverse_lazy('main:find'))
        # Так как в sqlite, используемой в django, поиск без учета регистра не работает с кириллицей
        # придётся реализовать поиск самому, используя цикл для проверки отдельных элементов
        find_groups = []
        for group in TestGroup.objects.all():
            group_title = group.title.lower()
            if group_title.find(find_text) != (-1):
                find_groups.append(group)

        find_tests = []
        for test in Test.objects.all():
            test_title = test.title.lower()
            if test_title.find(find_text) != (-1):
                find_tests.append(test)

        context = {'find_text': find_text, 'groups': find_groups, 'tests': find_tests}
        return render(request, 'main/result_find_page.html', context)


# Контроллер для обслуживания программного интерфейса (пока оставлен пустым)
def api_controller(request):
    return HttpResponseRedirect(reverse_lazy('main:index'))


# Контроллер регистрации
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse_lazy('main:index'))

    if request.method == 'GET':
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'main/register_user.html', context)


# Контроллер изменения данных пользователя
@login_required(login_url=reverse_lazy('main:login'))
def edit_account(request):
    if request.method == 'GET':
        form = UserEditForm(instance=request.user)
    if request.method == 'POST':
        user = request.user
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('main:account'))

    context = {'form': form}
    return render(request, 'main/edit_account_data.html', context)


# Контроллер входа
class LoginController(LoginView):
    template_name = 'main/login.html'


# Контроллер выхода
class LogoutController(LogoutView):
    next_page = reverse_lazy('main:index')


# Контроллер смены пароля
class PasswordChangeController(PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:account')
