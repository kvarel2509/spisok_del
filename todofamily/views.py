from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value
from django.db.models.functions import Now
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, View, FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from .forms import *
from .utils import InfoMixin
from django.utils import timezone
from django.contrib import messages


class InTodoView(InfoMixin):
    """Смотреть входящие задачи"""
    title = 'Входящие задачи'

    def get_queryset(self):
        return Todo.objects.filter(is_to=self.request.user, is_ok=False, is_negative=False).annotate(
            color=Case(
                When(data_deadline__lt=Now(), then=Value('warning')),
                default=Value('')
            )).select_related('is_from__userinfo', 'is_to')


class OutTodoView(InfoMixin):
    """Смотреть исходящие задачи"""
    title = 'Исходящие задачи'

    def get_queryset(self):
        return Todo.objects.filter(is_from=self.request.user).exclude(is_to=self.request.user).annotate(
            color=Case(
                When(is_ok=True, then=Value('success')),
                When(is_negative=True, then=Value('danger')),
                When(data_deadline__lt=Now(), then=Value('warning'))
            )
        ).select_related('is_from__userinfo', 'is_to')


class ISuccessTodo(InfoMixin):
    title = 'Список исполненных мной задач'

    def get_queryset(self):
        return Todo.objects.filter(is_to=self.request.user, is_ok=True).annotate(color=Value('success')).select_related(
            'is_from__userinfo', 'is_to'
        )


class YouSuccessTodo(InfoMixin):
    title = 'Список исполненных не мной задач'

    def get_queryset(self):
        return Todo.objects.filter(
            is_from=self.request.user, is_ok=True
        ).exclude(is_to=self.request.user).annotate(color=Value('success')).select_related('is_from__userinfo', 'is_to')


class INegativeTodo(InfoMixin):
    title = 'Список отклоненных мной задач'

    def get_queryset(self):
        return Todo.objects.filter(is_to=self.request.user, is_negative=True).annotate(
            color=Value('danger')).select_related('is_from__userinfo', 'is_to')


class IDelayTodo(InfoMixin):
    title = 'Просроченные мной задачи'

    def get_queryset(self):
        return Todo.objects.filter(
            is_to=self.request.user, data_deadline__lt=timezone.now(), is_ok=False, is_negative=False).annotate(
            color=Value('warning')).select_related('is_from__userinfo', 'is_to')


class YouDelayTodo(InfoMixin):
    title = 'Просроченные другими задачи'

    def get_queryset(self):
        return Todo.objects.filter(is_from=self.request.user, data_deadline__lt=timezone.now()).exclude(
            is_to=self.request.user).annotate(color=Value('warning')).select_related('is_from__userinfo', 'is_to')


class YouNegativeTodo(InfoMixin):
    title = 'Список отклоненных не мной задач'

    def get_queryset(self):
        return Todo.objects.filter(is_from=self.request.user, is_negative=True).exclude(
            is_to=self.request.user).annotate(color=Value('danger')).select_related('is_from__userinfo', 'is_to')


class DeleteTodo(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return redirect(reverse_lazy('all_todo'))


class CreateTodo(LoginRequiredMixin, CreateView):
    form_class = NewTodo
    template_name = 'todofamily/create_todo.html'
    extra_context = {'title': 'Создание задачи'}
    success_url = reverse_lazy('all_todo')

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно создана')
        form.instance.is_from = self.request.user
        return super().form_valid(form)


def otzyv(request):
    if request.method == 'POST':
        form = Otzyv(request.POST)
        if form.is_valid():
            return redirect('all_todo')
    else:
        form = Otzyv()
    return render(request, 'todofamily/otzyv.html', context={'form': form})


class ShowTodoView(LoginRequiredMixin, DetailView):
    template_name = 'todofamily/detail.html'
    context_object_name = 'data'
    model = Todo
    ref_url = 'all_todo'

    def get_ref_url(self):
        if self.request.META['HTTP_REFERER']:
            return self.request.META['HTTP_REFERER']
        return self.ref_url

    def get_context_data(self, **kwargs):
        self.object.is_scan = True
        self.object.save()
        self.ref_url = self.get_ref_url()
        context = super().get_context_data(**kwargs)
        context['title'] = f'Задача №{self.object.pk}'
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(todo__pk=self.object.pk)
        return context


class SuccessTodo(LoginRequiredMixin, View):

    def get(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.is_ok = True
        todo.save()
        Comment.objects.create(user=self.request.user, todo=todo, content='Задача закрыта мной как исполненная')
        return redirect(reverse_lazy('all_todo'))


class EditTodo(LoginRequiredMixin, UpdateView):
    template_name = 'todofamily/create_todo.html'
    form_class = NewTodo
    model = Todo

    def get_success_url(self):
        Comment.objects.create(user=self.request.user, todo=self.object, content='В задачу внесены изменения')
        return reverse_lazy('show_todo', kwargs={'pk': self.object.pk})


class NegativeTodo(LoginRequiredMixin, View):

    def get(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.is_negative = True
        todo.save()
        Comment.objects.create(user=self.request.user, todo=todo, content='Задача закрыта мной как отклоненная')
        return redirect(reverse_lazy('all_todo'))


class ReturnTodo(LoginRequiredMixin, View):

    def get(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.is_ok = False
        todo.is_negative = False
        todo.save()
        Comment.objects.create(user=self.request.user, todo=todo, content='Задача возвращена в работу')
        return redirect(reverse_lazy('all_todo'))


class ShowTodoFormComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    form_class = CommentForm
    model = Todo
    template_name = 'todofamily/detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.todo = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('show_todo', kwargs={'pk': self.object.pk})


class ShowTodo(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        func = ShowTodoView.as_view()
        return func(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        func = ShowTodoFormComment.as_view()
        return func(request, *args, **kwargs)


class RegUser(CreateView):
    """Регистрация"""

    form_class = RegistrationForm
    template_name = 'todofamily/reg.html'
    extra_context = {'title': 'Страница регистрации нового пользователя'}

    def form_valid(self, form):
        a = super().form_valid(form)
        UserInfo.objects.create(user=self.object)
        return a

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('all_todo')


class AuthUser(LoginView):
    """Авторизация"""

    form_class = AuthForm
    template_name = 'todofamily/auth.html'
    extra_context = {'title': 'Страница входа'}

    def get_success_url(self):
        return reverse_lazy('all_todo')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('auth')


class AccountView(LoginRequiredMixin, UpdateView):
    """Показывает настройки профиля"""

    form_class = AccountForm
    template_name = 'todofamily/account.html'
    extra_context = {'title': 'Настройка профиля'}
    success_url = reverse_lazy('in_todo')

    def get_object(self, queryset=None):
        return UserInfo.objects.get(user=self.request.user)

    def get_initial(self):
        user = self.request.user
        return {'username': user.username, 'first_name': user.first_name}


class PasswordEditView(LoginRequiredMixin, PasswordChangeView):
    """Изменить пароль"""

    template_name = 'todofamily/passwordedit.html'
    success_url = reverse_lazy('account')
    form_class = PasswordEdit
