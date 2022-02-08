from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', InTodoView.as_view(), name='all_todo'),
    path('in_todo/', InTodoView.as_view(), name='in_todo'),
    path('out_todo/', OutTodoView.as_view(), name='out_todo'),
    path('i_delay_todo/', IDelayTodo.as_view(), name='i_delay_todo'),
    path('you_delay_todo/', YouDelayTodo.as_view(), name='you_delay_todo'),
    path('out_todo/', OutTodoView.as_view(), name='out_todo'),
    path('i_success_todo/', ISuccessTodo.as_view(), name='i_success_todo'),
    path('you_success_todo/', YouSuccessTodo.as_view(), name='you_success_todo'),
    path('i_negative_todo/', INegativeTodo.as_view(), name='i_negative_todo'),
    path('you_negative_todo/', YouNegativeTodo.as_view(), name='you_negative_todo'),
    path('new/', CreateTodo.as_view(), name='create_todo'),
    path('show/<int:pk>/', ShowTodo.as_view(), name='show_todo'),
    path('show/<int:pk>/ok/', SuccessTodo.as_view(), name='success_todo'),
    path('show/<int:pk>/edit/', EditTodo.as_view(), name='edit_todo'),
    path('show/<int:pk>/negative/', NegativeTodo.as_view(), name='negative_todo'),
    path('show/<int:pk>/return/', ReturnTodo.as_view(), name='return_todo'),
    path('show/<int:pk>/delete/', DeleteTodo.as_view(), name='delete_todo'),
    path('new_otzyv/', otzyv, name='otzyv'),
    path('login/', RegUser.as_view(), name='login'),
    path('auth/', AuthUser.as_view(), name='auth'),
    path('logout/', Logout.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('account/passwordchange/', PasswordEditView.as_view(), name='PasswordEdit')
    ]