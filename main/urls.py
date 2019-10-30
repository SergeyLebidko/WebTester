from django.urls import path
from .views import index, test_list

app_name = 'main'

urlpatterns = [
    path('<int:test_group_id>/', test_list, name='test_list'),
    path('', index, name='index')

]
