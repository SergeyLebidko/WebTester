from django.urls import path
from .views import index, test_list, test_page

app_name = 'main'

urlpatterns = [
    path('<int:test_group_id>/<int:test_id>/', test_page, name='test_page'),
    path('<int:test_group_id>/', test_list, name='test_list'),
    path('', index, name='index')

]
