from django.urls import path
from .views import index, test_list, test_page, LoginController, LogoutController

app_name = 'main'

urlpatterns = [
    path('<int:test_group_id>/<int:test_id>/', test_page, name='test_page'),
    path('<int:test_group_id>/', test_list, name='test_list'),
    path('logout/', LogoutController.as_view(), name='logout'),
    path('login/', LoginController.as_view(), name='login'),
    path('', index, name='index')

]
