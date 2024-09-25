from django.contrib import admin

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Post

@admin.action(description='Удалить все посты')
def delete_all_posts(modeladmin, request, queryset):
    Post.objects.all().delete()

class PostAdmin(admin.ModelAdmin):
    actions = [delete_all_posts]

admin.site.register(Post, PostAdmin)


# Register your models here.
