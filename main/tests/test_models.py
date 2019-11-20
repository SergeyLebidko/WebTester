from django.test import TestCase
from main.models import TestGroup


class GroupTester(TestCase):

    @classmethod
    def setUpTestData(cls):
        TestGroup.objects.create(title='Тестирование в Django')

    # Тест проверяет правильность вывода метода __str__ в модели групп тестов
    def test_str(self):
        group = TestGroup.objects.get(pk=1)
        self.assertEqual(group.title, 'Тестирование в Django')

    # Тест проверяет корректность указания отображаемого имени моели групп тестов
    def test_verbose_name(self):
        group = TestGroup.objects.get(pk=1)
        verbose_name = group._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Группа тестов')
