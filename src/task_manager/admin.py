from django.contrib import admin
from django.utils.safestring import mark_safe
from task_manager.models import Tasks, Tags, Projects, ProjectDetails,Comments, Attachments


class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1

class AttachmentsInline(admin.StackedInline):
    model = Attachments
    extra = 1

class ProjectDetailsInline(admin.TabularInline): #т.к. связть OneToOne более компактно подходит этот тип
    model = ProjectDetails
    extra = 0

class TagsInline(admin.TabularInline):
    model = Tags.tasks.through
    extra = 1

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    fields = (('name', 'status'),
              'description',
              'priority',
              'project',
              'assignee',
              'count_comments',
              'created_at',
              'is_reopened',
              )
    list_display = ('name',
                    'status',
                    'priority',
                    'project',
                    'display_assignee',
                    'name_with_status',
                    )
    list_display_links = ('name',
                          )
    list_editable = ('priority',
                     'status',
                     )
    list_filter = ('status',
                   'priority',
                   'project',
                   'assignee',
                   )
    search_fields = ('name',
                     )
    readonly_fields = ('count_comments',
                       'created_at',
                       )
    list_per_page = 20
    inlines = (CommentsInline,
               AttachmentsInline,
               TagsInline,
               )
    actions = ('make_completed',
               'make_cancelled',
               'reset_reopened',
               'create_comment',
               )
    save_on_top = True

    def name_with_status(self, obj):
        return f"{obj.name} ({ obj.status})"
    name_with_status.short_description = "Название и статус"

    @admin.display(description="Исполнитель", ordering="assignee__email")
    def display_assignee(self, instance):
        return f"{instance.assignee}"

    @admin.display(description="Количество комментариев")
    def count_comments(self, obj):
        return obj.comments.count()

    @admin.action(description="Завершить задачи")
    def make_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description="Отменить задачи")
    def make_cancelled(self, request, queryset):
        queryset.update(status='cancelled')

    @admin.action(description="Сбросить переоткрытие")
    def reset_reopened(self, request, queryset):
        for obj in queryset:
            obj.is_reopened = False
            obj.save()

    @admin.action(description="Создать комментарий")
    def create_comment(self, request, queryset):
        for obj in queryset:
            obj.comments.create(message='Processed by admin',
                                user=obj.assignee,
                                )


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    # fields = ('name', 'description')
    exclude = ('owner',)
    inlines = (ProjectDetailsInline, )


class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'task',
                    'file',
                    'display_picture',
                    'picture',
                    )
    list_filter = ("task",)
    list_per_page = 5

    @admin.display(description="Отображение картинки")
    def display_picture(self, instance):
        if instance.picture:
            return mark_safe(f"<img src ={ instance.picture.url } width=150 />")

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(Tags)
admin.site.register(ProjectDetails)
admin.site.register(Comments)
admin.site.register(Attachments, AttachmentsAdmin)

# Register your models here.
