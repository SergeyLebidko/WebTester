from django.test import TestCase
from main.models import TestGroup
from django.urls import reverse


class IndexTester(TestCase):

    @classmethod
    def setUpTestData(cls):
        group_names = ['Java', 'Python', 'SQL', 'C++', 'JavaScript', 'PHP', 'HTML/CSS']
        for group_name in group_names:
            TestGroup.objects.create(title=group_name)

    # Проверяем доступность контроллера по url
    def test_status_on_url(self):
        resp = self.client.get('/main/')
        self.assertEqual(resp.status_code, 200)

    # Проверяем правильность обратного разрешения url
    def test_status_on_reverse_url(self):
        resp = self.client.get(reverse('main:index'))
        self.assertEqual(resp.status_code, 200)

    # Проверяем наличие необходимых данных в контексте главной страницы
    def test_context(self):
        resp = self.client.get(reverse('main:index'))
        self.assertTrue('test_groups' in resp.context)
        self.assertTrue(len(resp.context['test_groups']) == 7)
