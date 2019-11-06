from django.urls import path
from .views import index, test_list, test_page, LoginController, LogoutController, register_user, statistic_page, \
    find_page

app_name = 'main'

urlpatterns = [
    path('<int:test_group_id>/<int:test_id>/', test_page, name='test_page'),
    path('<int:test_group_id>/', test_list, name='test_list'),
    path('logout/', LogoutController.as_view(), name='logout'),
    path('login/', LoginController.as_view(), name='login'),
    path('register/', register_user, name='register_user'),
    path('user_statistic/', statistic_page, name='statistic_page'),
    path('find/', find_page, name='find'),
    path('', index, name='index')
]
