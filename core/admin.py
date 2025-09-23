from django.contrib import admin
from .models import jobApplication, StatusHistory, interviewLog, ResumeAnalysis

class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ('changed_at',)

class interviewLogInline(admin.TabularInline):
    model = interviewLog
    extra = 0
    


@admin.register(jobApplication)
class jobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'user', 'status', 'date_applied', 'created_at')
    list_filter = ('status', 'source' )
    search_fields = ('company', 'role', 'notes')
    inlines = [StatusHistoryInline, interviewLogInline]
    

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('job', 'match_score', 'analysis_date')    
    

admin.site.register(StatusHistory)
admin.site.register(interviewLog)

