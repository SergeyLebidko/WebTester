from django.shortcuts import render
from .models import TestGroup, Test


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
    selected_group = TestGroup.objects.get(pk=test_group_id)
    selected_test = Test.objects.get(pk=test_id)
    context = {'selected_group': selected_group, 'selected_test': selected_test}
    return render(request, 'main/test_page.html', context)
