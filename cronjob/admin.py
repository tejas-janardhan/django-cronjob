from django.contrib import admin
from .models import JobGroup, Job, JobHistory


# Register your models here.

class JobGroupAdmin(admin.ModelAdmin):
    model = JobGroup
    fields = ['name', 'status', 'time_duration', 'duration_unit', 'jobs', 'cron_script']
    readonly_fields = ['cron_script']
    filter_horizontal = ['jobs']

    def cron_script(self, obj):
        return obj.get_cron_script()


class JobHistoryAdmin(admin.ModelAdmin):
    model = JobHistory
    fields = ['date_started', 'date_ended', 'status', 'exception', 'job', 'job_group', 'time_interval']
    readonly_fields = ['date_started', 'date_ended', 'status', 'exception', 'job', 'job_group', 'time_interval']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(JobGroup, JobGroupAdmin)
admin.site.register(Job)
admin.site.register(JobHistory, JobHistoryAdmin)
