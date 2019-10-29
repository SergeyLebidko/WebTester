from django.db import models


# Группа тестов
class TestGroup(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False, blank=False, verbose_name='Группа тестов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа тестов'
        verbose_name_plural = 'Группы тестов'
        ordering = ['title']


# Тест
class Test(models.Model):
    title = models.CharField(max_length=200, unique=False, null=False, blank=False, verbose_name='Название теста')
    test_group = models.ForeignKey(TestGroup, on_delete=models.CASCADE, null=False, blank=False,
                                   verbose_name='Группа тестов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['title']


# Вопрос теста
class Question(models.Model):
    title = models.CharField(max_length=1000, null=False, blank=False, verbose_name='Вопрос')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Название теста')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['title']


# Вариант ответа
class Answer(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Вариант ответа')
    is_correct = models.BooleanField(null=False, blank=False, default=False, verbose_name='Верный ответ')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Вопрос')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ['title']
