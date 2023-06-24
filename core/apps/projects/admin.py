from django.contrib import admin
from .models import Category, Project, Attachment, Link, Comment, LikeDislike
from django.conf import settings
from django_admin_inline_paginator.admin import TabularInlinePaginated


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug', 'id']
    fieldsets = [
        (None, {'fields': ['id', 'name', 'icon', 'slug']}),
    ]


class AttachmentInline(admin.StackedInline):
    readonly_fields = ['name', ]
    model = Attachment
    extra = 0
    max_num = settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT


class LinkInline(admin.StackedInline):
    readonly_fields = ['url', ]
    model = Link
    fieldsets = [
        (None, {'fields': ['url']}),
    ]
    extra = 0
    max_num = settings.MAX_NUMBER_OF_LINKS_PER_PROJECT


class CommentInline(TabularInlinePaginated):
    readonly_fields = ['likes_count', 'dislikes_count', 'rating', 'parent']
    fields = ('account', 'content', 'parent')
    can_delete = True
    model = Comment
    per_page = 20


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['is_personal', 'created_at', 'updated_at', 'likes_count', 'dislikes_count', 'rating']
    fieldsets = [
        (None,
         {'fields': ['account', 'category', 'description']}),
        ('Рейтинг',
         {'fields': ['likes_count', 'dislikes_count', 'rating']}),
        ('Опции',
         {'fields': ['is_approved', 'is_feature', 'is_personal']}),
        ('Даты',
         {'fields': ['created_at', 'updated_at']}),
    ]
    inlines = [AttachmentInline, LinkInline, CommentInline]
    list_display = ('created_at', 'category', 'is_approved', 'rating')
    list_filter = ['created_at', 'category', 'is_feature', 'is_approved']
    search_fields = ['description', 'account__phone_number', 'category__name']


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'likes_count', 'dislikes_count', 'rating']
    fieldsets = [
        (None,
         {'fields': ['account', 'project', 'content', 'parent']}),
        ('Рейтинг',
         {'fields': ['likes_count', 'dislikes_count', 'rating']}),
        ('Даты',
         {'fields': ['created_at', 'updated_at']}),
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(LikeDislike)
admin.site.register(Comment, CommentAdmin)
