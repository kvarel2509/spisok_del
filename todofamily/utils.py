from django.urls import reverse_lazy

from .models import Todo
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime


class InfoMixin(LoginRequiredMixin, ListView):
    """Добавляем в миксин, который создаст дополнительные поля для контекста"""
    model = Todo
    context_object_name = 'todo'
    title = 'Home'
    template_name = 'todofamily/index.html'
    paginate_by = 10
    login_url = reverse_lazy('auth')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

