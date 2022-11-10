from django.contrib import admin

from goals.models import (Board, BoardParticipant, Goal, GoalCategory,
                          GoalComment)


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created', 'updated', 'is_deleted')
    list_display_links = ('title',)
    search_fields = ('title', 'user')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'priority')
    list_display_links = ('title',)
    search_fields = ('title', 'description')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text')
    list_display_links = ('text',)
    search_fields = ('text',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted')

@admin.register(BoardParticipant)
class BoardParticipant(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')
