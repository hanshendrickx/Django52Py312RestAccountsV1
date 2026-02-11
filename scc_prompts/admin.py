from django.contrib import admin
from .models import PatientComplaint, AIPrompt, PromptTemplate


@admin.register(PatientComplaint)
class PatientComplaintAdmin(admin.ModelAdmin):
    list_display = ['patient_identifier', 'chief_complaint', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['patient_identifier', 'chief_complaint', 'signs_symptoms']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AIPrompt)
class AIPromptAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'prompt_type', 'created_at']
    list_filter = ['prompt_type', 'created_at']
    search_fields = ['generated_prompt', 'complaint__patient_identifier']
    readonly_fields = ['created_at']


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
