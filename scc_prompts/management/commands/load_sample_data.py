from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from scc_prompts.models import PatientComplaint, PromptTemplate
from scc_prompts.services import PromptGenerator

User = get_user_model()


class Command(BaseCommand):
    help = 'Load sample patient complaints and prompt templates for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create or get demo user
        user, created = User.objects.get_or_create(
            username='demo_doctor',
            defaults={
                'email': 'demo@example.com',
                'is_staff': False,
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created demo user: {user.username}'))
        
        # Create sample complaints
        complaints_data = [
            {
                'patient_identifier': 'P001',
                'chief_complaint': 'Chest pain',
                'signs_symptoms': 'Sharp chest pain radiating to left arm, diaphoresis, shortness of breath',
                'history_present_illness': 'Sudden onset 2 hours ago while watching TV. Pain score 8/10.',
                'relevant_medical_history': 'Hypertension, diabetes mellitus type 2, active smoker (20 pack-years)',
            },
            {
                'patient_identifier': 'P002',
                'chief_complaint': 'Severe headache',
                'signs_symptoms': 'Sudden onset worst headache of life, photophobia, neck stiffness',
                'history_present_illness': 'Woke up with headache this morning, progressively worsening over 4 hours',
                'relevant_medical_history': 'No significant medical history, takes oral contraceptives',
            },
            {
                'patient_identifier': 'P003',
                'chief_complaint': 'Abdominal pain',
                'signs_symptoms': 'Right lower quadrant pain, nausea, vomiting, fever (38.5°C)',
                'history_present_illness': 'Started with periumbilical pain 12 hours ago, now localized to RLQ',
                'relevant_medical_history': 'Appendectomy ruled out (patient still has appendix)',
            },
        ]
        
        created_count = 0
        for complaint_data in complaints_data:
            complaint, created = PatientComplaint.objects.get_or_create(
                patient_identifier=complaint_data['patient_identifier'],
                created_by=user,
                defaults=complaint_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created complaint: {complaint.patient_identifier}')
                
                # Generate a combined prompt for demonstration
                ai_prompt = PromptGenerator.create_ai_prompt(complaint.id, 'combined')
                self.stdout.write(f'  Generated AI prompt for {complaint.patient_identifier}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new complaints'))
        
        # Create sample templates
        templates_data = [
            {
                'name': 'Emergency Triage Template',
                'description': 'Standard template for emergency department triage',
                'template_text': '''Patient: {patient_identifier}
Chief Complaint: {chief_complaint}
Signs & Symptoms: {signs_symptoms}

Triage Assessment Required:
1. Urgency level (ESI 1-5)
2. Vital signs priority
3. Immediate interventions needed''',
            },
            {
                'name': 'Guidelines Review Template',
                'description': 'Template for clinical guidelines consultation',
                'template_text': '''Case ID: {patient_identifier}
Presenting Complaint: {chief_complaint}

Clinical Guidelines Request:
Please provide evidence-based guidelines for:
- Diagnostic approach
- Treatment protocols
- Follow-up care''',
            },
        ]
        
        template_count = 0
        for template_data in templates_data:
            template, created = PromptTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                template_count += 1
                self.stdout.write(f'  Created template: {template.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {template_count} new templates'))
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write(f'\nDemo user credentials:')
        self.stdout.write(f'  Username: demo_doctor')
        self.stdout.write(f'  Password: demo123')
