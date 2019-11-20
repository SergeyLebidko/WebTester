from django.test import TestCase
from main.forms import UserRegisterForm


class RegisterTester(TestCase):

    # Тест проверяет обязательность заполнения полей с именем и фамилией формы регистрации нового пользователя
    def test_first_and_last_names(self):
        form_data = {
            'first_name': '',
            'last_name': '',
        }
        form = UserRegisterForm(data=form_data)
        form.is_valid()
        self.assertTrue(form.errors['first_name'].data[0].message == 'Это поле обязательно для заполнения.' and
                        form.errors['last_name'].data[0].message == 'Это поле обязательно для заполнения.')
