from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import TestGroup, Test


# Контроллер главной страницы
def index(request):
    test_groups = TestGroup.objects.all()
    context = {'test_groups': test_groups}
    return render(request, 'main/index.html', context)


# Контроллер страницы со списком тестов
def test_list(request, test_group_id):
    try:
        selected_group = TestGroup.objects.get(pk=test_group_id)
    except (TestGroup.DoesNotExist, TestGroup.MultipleObjectsReturned):
        return HttpResponseBadRequest()
    tests = Test.objects.filter(test_group=selected_group)
    context = {'tests': tests, 'selected_group': selected_group}
    return render(request, 'main/test_list.html', context)
