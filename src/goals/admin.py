from django.contrib import admin

from goals.models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created', 'updated', 'is_deleted')
    list_display_links = ('title',)
    search_fields = ('title', 'user')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'priority')
    list_display_links = ('title',)
    search_fields = ('title', 'description')


admin.site.register(GoalCategory, GoalCategoryAdmin, GoalAdmin)
