from django.contrib import admin
from django.utils.safestring import mark_safe
from task_manager.models import Tasks, Tags, Projects, ProjectDetails,Comments, Attachments


class TasksAdmin(admin.ModelAdmin):

    @admin.display(description="Наименование")
    def display_name(self, instance):
        return mark_safe(f"<h1>{instance.name}</h1>")



admin.site.register(Tasks)
admin.site.register(Tags)
admin.site.register(Projects)
admin.site.register(ProjectDetails)
admin.site.register(Comments)
admin.site.register(Attachments)

# Register your models here.
