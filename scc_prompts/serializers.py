from rest_framework import serializers
from .models import PatientComplaint, AIPrompt, PromptTemplate


class PatientComplaintSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = PatientComplaint
        fields = [
            'id',
            'created_by',
            'created_by_username',
            'patient_identifier',
            'chief_complaint',
            'signs_symptoms',
            'history_present_illness',
            'relevant_medical_history',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class AIPromptSerializer(serializers.ModelSerializer):
    complaint_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = AIPrompt
        fields = [
            'id',
            'complaint',
            'complaint_summary',
            'prompt_type',
            'generated_prompt',
            'triage_context',
            'guidelines_context',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_complaint_summary(self, obj):
        return f"{obj.complaint.patient_identifier} - {obj.complaint.chief_complaint}"


class PromptTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptTemplate
        fields = [
            'id',
            'name',
            'description',
            'template_text',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GeneratePromptSerializer(serializers.Serializer):
    """
    Serializer for the prompt generation endpoint.
    Takes a complaint ID and generates appropriate AI prompts.
    """
    complaint_id = serializers.IntegerField()
    prompt_type = serializers.ChoiceField(
        choices=['triage', 'guidelines', 'combined'],
        default='combined'
    )
    include_triage_context = serializers.BooleanField(default=True)
    include_guidelines_context = serializers.BooleanField(default=True)
