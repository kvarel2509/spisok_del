from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *
# Register your models here.


class Todoadmin(admin.ModelAdmin):
    list_display = ('pk', 'is_from', 'is_to', 'content', 'data_update')
    list_filter = ('is_from', 'is_to')
    prepopulated_fields = {'slug': ('content',)}


class Commentsadmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    list_display_links = ('user',)
    search_fields = ('user',)


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'


class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Todo, Todoadmin)
admin.site.register(Comment, Commentsadmin)

