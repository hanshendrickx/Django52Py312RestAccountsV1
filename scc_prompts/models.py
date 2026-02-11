from django.db import models
from django.conf import settings


class PatientComplaint(models.Model):
    """
    Model to store patient Signs & Current Complaints (SCC).
    This represents the 'S' (Subjective) part of the SOAP methodology.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    patient_identifier = models.CharField(
        max_length=100,
        help_text="Patient identifier or case number"
    )
    chief_complaint = models.CharField(
        max_length=500,
        help_text="Main complaint or reason for consultation"
    )
    signs_symptoms = models.TextField(
        help_text="Detailed signs and symptoms reported by patient"
    )
    history_present_illness = models.TextField(
        blank=True,
        help_text="History of present illness (HPI)"
    )
    relevant_medical_history = models.TextField(
        blank=True,
        help_text="Relevant past medical history"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient_identifier} - {self.chief_complaint[:50]}"


class AIPrompt(models.Model):
    """
    Model to store generated AI prompts for Mock Triage and Guidelines.
    These are professional-level prompts used in Grand Rounds style meetings.
    """
    PROMPT_TYPE_CHOICES = [
        ('triage', 'Mock Triage'),
        ('guidelines', 'Mock Guidelines'),
        ('combined', 'Combined Pro-Prompt'),
    ]

    complaint = models.ForeignKey(
        PatientComplaint,
        on_delete=models.CASCADE,
        related_name='ai_prompts'
    )
    prompt_type = models.CharField(
        max_length=20,
        choices=PROMPT_TYPE_CHOICES,
        default='combined'
    )
    generated_prompt = models.TextField(
        help_text="The AI-ready prompt combining subjective data and professional context"
    )
    triage_context = models.TextField(
        blank=True,
        help_text="Additional context for triage decision-making"
    )
    guidelines_context = models.TextField(
        blank=True,
        help_text="Clinical guidelines and protocols to consider"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prompt_type} - {self.complaint.patient_identifier}"


class PromptTemplate(models.Model):
    """
    Model to store reusable prompt templates for different scenarios.
    Templates can be used to generate consistent professional prompts.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    template_text = models.TextField(
        help_text="Template with placeholders like {chief_complaint}, {signs_symptoms}, etc."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
