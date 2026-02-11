from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import PatientComplaint, AIPrompt, PromptTemplate
from .services import PromptGenerator

User = get_user_model()


class PatientComplaintModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testdoc',
            email='testdoc@example.com',
            password='testpass123'
        )
        
    def test_create_patient_complaint(self):
        """Test creating a patient complaint"""
        complaint = PatientComplaint.objects.create(
            created_by=self.user,
            patient_identifier='P001',
            chief_complaint='Chest pain',
            signs_symptoms='Sharp chest pain, radiating to left arm',
            history_present_illness='Started 2 hours ago',
            relevant_medical_history='Hypertension'
        )
        self.assertEqual(complaint.patient_identifier, 'P001')
        self.assertEqual(str(complaint), 'P001 - Chest pain')
        
    def test_complaint_ordering(self):
        """Test that complaints are ordered by created_at descending"""
        complaint1 = PatientComplaint.objects.create(
            created_by=self.user,
            patient_identifier='P001',
            chief_complaint='First',
            signs_symptoms='Test'
        )
        complaint2 = PatientComplaint.objects.create(
            created_by=self.user,
            patient_identifier='P002',
            chief_complaint='Second',
            signs_symptoms='Test'
        )
        complaints = PatientComplaint.objects.all()
        self.assertEqual(complaints[0], complaint2)


class AIPromptModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testdoc',
            email='testdoc@example.com',
            password='testpass123'
        )
        self.complaint = PatientComplaint.objects.create(
            created_by=self.user,
            patient_identifier='P001',
            chief_complaint='Chest pain',
            signs_symptoms='Sharp chest pain'
        )
        
    def test_create_ai_prompt(self):
        """Test creating an AI prompt"""
        prompt = AIPrompt.objects.create(
            complaint=self.complaint,
            prompt_type='triage',
            generated_prompt='Test prompt'
        )
        self.assertEqual(prompt.prompt_type, 'triage')
        self.assertIn('P001', str(prompt))


class PromptTemplateModelTest(TestCase):
    def test_create_template(self):
        """Test creating a prompt template"""
        template = PromptTemplate.objects.create(
            name='Standard Triage',
            description='Standard triage template',
            template_text='Patient: {patient_identifier}'
        )
        self.assertEqual(template.name, 'Standard Triage')
        self.assertTrue(template.is_active)


class PromptGeneratorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testdoc',
            email='testdoc@example.com',
            password='testpass123'
        )
        self.complaint = PatientComplaint.objects.create(
            created_by=self.user,
            patient_identifier='P001',
            chief_complaint='Chest pain',
            signs_symptoms='Sharp chest pain, radiating to left arm',
            history_present_illness='Started 2 hours ago',
            relevant_medical_history='Hypertension, smoker'
        )
    
    def test_generate_triage_prompt(self):
        """Test triage prompt generation"""
        prompt = PromptGenerator.generate_triage_prompt(self.complaint)
        self.assertIn('P001', prompt)
        self.assertIn('Chest pain', prompt)
        self.assertIn('Mock Triage', prompt)
        self.assertIn('Urgency level', prompt)
        
    def test_generate_guidelines_prompt(self):
        """Test guidelines prompt generation"""
        prompt = PromptGenerator.generate_guidelines_prompt(self.complaint)
        self.assertIn('P001', prompt)
        self.assertIn('Clinical Guidelines', prompt)
        self.assertIn('Evidence-based', prompt)
        
    def test_generate_combined_prompt(self):
        """Test combined prompt generation"""
        prompt = PromptGenerator.generate_combined_prompt(self.complaint)
        self.assertIn('P001', prompt)
        self.assertIn('Grand Rounds', prompt)
        self.assertIn('Triage Assessment', prompt)
        self.assertIn('Clinical Guidelines', prompt)
        
    def test_create_ai_prompt_triage(self):
        """Test creating and saving a triage AI prompt"""
        ai_prompt = PromptGenerator.create_ai_prompt(self.complaint.id, 'triage')
        self.assertEqual(ai_prompt.prompt_type, 'triage')
        self.assertEqual(ai_prompt.complaint, self.complaint)
        self.assertIn('Mock Triage', ai_prompt.generated_prompt)
        
    def test_create_ai_prompt_combined(self):
        """Test creating and saving a combined AI prompt"""
        ai_prompt = PromptGenerator.create_ai_prompt(self.complaint.id, 'combined')
        self.assertEqual(ai_prompt.prompt_type, 'combined')
        self.assertIn('Grand Rounds', ai_prompt.generated_prompt)
        
    def test_create_ai_prompt_invalid_id(self):
        """Test that creating prompt with invalid complaint ID raises error"""
        with self.assertRaises(ValueError):
            PromptGenerator.create_ai_prompt(9999, 'triage')
