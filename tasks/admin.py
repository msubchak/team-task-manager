from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, Task, Worker, Position, Tag, Project, Team

admin.site.register(TaskType)
admin.site.register(Position)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Team)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_complete",
        "priority",
        "task_type",
        "project",
    )
    list_filter = ("is_complete", "priority", "task_type", "deadline",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional information"), {"fields": ("position", "team",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "position",
                        "team"
                    )
                },
            ),
        )
    )
