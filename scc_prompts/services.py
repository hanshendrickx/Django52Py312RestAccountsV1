"""
Service module for generating AI prompts from patient complaints.
This module contains the core logic for creating professional-level prompts
suitable for Mock Triage and Guidelines generation.
"""
from .models import PatientComplaint, AIPrompt, PromptTemplate


class PromptGenerator:
    """
    Service class for generating AI prompts from patient complaints.
    """
    
    @staticmethod
    def generate_triage_prompt(complaint: PatientComplaint) -> str:
        """
        Generate a Mock Triage prompt from patient complaint data.
        """
        prompt = f"""# Mock Triage Assessment

**Patient Case ID:** {complaint.patient_identifier}

**Chief Complaint:** {complaint.chief_complaint}

**Signs & Symptoms:**
{complaint.signs_symptoms}
"""
        
        if complaint.history_present_illness:
            prompt += f"""
**History of Present Illness:**
{complaint.history_present_illness}
"""
        
        if complaint.relevant_medical_history:
            prompt += f"""
**Relevant Medical History:**
{complaint.relevant_medical_history}
"""
        
        prompt += """
**Triage Assessment Request:**
Based on the above subjective information (S - Subjective part of SOAP), please provide:
1. Urgency level assessment (Critical/High/Medium/Low)
2. Recommended immediate actions
3. Red flags or concerning features
4. Suggested clinical pathway
5. Differential diagnoses to consider

Please provide a professional triage assessment as would be discussed in a Grand Rounds meeting.
"""
        return prompt
    
    @staticmethod
    def generate_guidelines_prompt(complaint: PatientComplaint) -> str:
        """
        Generate a Mock Guidelines prompt from patient complaint data.
        """
        prompt = f"""# Clinical Guidelines Consultation

**Patient Case ID:** {complaint.patient_identifier}

**Chief Complaint:** {complaint.chief_complaint}

**Signs & Symptoms:**
{complaint.signs_symptoms}
"""
        
        if complaint.history_present_illness:
            prompt += f"""
**History of Present Illness:**
{complaint.history_present_illness}
"""
        
        if complaint.relevant_medical_history:
            prompt += f"""
**Relevant Medical History:**
{complaint.relevant_medical_history}
"""
        
        prompt += """
**Guidelines Request:**
Based on the above subjective clinical information, please provide:
1. Applicable clinical practice guidelines
2. Evidence-based diagnostic approach
3. Recommended investigations/tests
4. Treatment protocols to consider
5. Follow-up recommendations
6. Patient safety considerations

Please reference current clinical guidelines and best practices as would be expected in a professional medical consultation.
"""
        return prompt
    
    @staticmethod
    def generate_combined_prompt(complaint: PatientComplaint) -> str:
        """
        Generate a combined Pro-Prompt for comprehensive AI assessment.
        """
        prompt = f"""# Professional Clinical Assessment - Grand Rounds Format

**Patient Case ID:** {complaint.patient_identifier}

**Chief Complaint:** {complaint.chief_complaint}

**Subjective (S) - Signs & Current Complaints (SCC):**
{complaint.signs_symptoms}
"""
        
        if complaint.history_present_illness:
            prompt += f"""
**History of Present Illness:**
{complaint.history_present_illness}
"""
        
        if complaint.relevant_medical_history:
            prompt += f"""
**Relevant Medical History:**
{complaint.relevant_medical_history}
"""
        
        prompt += """
**Professional Assessment Request (Pro-Prompt):**

This case is presented for comprehensive clinical evaluation combining both triage and guidelines review, as would be conducted in a Grand Rounds setting.

Please provide:

**A. Triage Assessment:**
1. Urgency level (Critical/High/Medium/Low) with justification
2. Immediate management priorities
3. Red flags and concerning features
4. Time-sensitive interventions

**B. Clinical Guidelines Review:**
1. Applicable evidence-based guidelines
2. Recommended diagnostic workup
3. Treatment protocols and algorithms
4. Quality and safety considerations

**C. Differential Diagnosis:**
1. Most likely diagnoses (prioritized)
2. Must-not-miss diagnoses
3. Supporting and contradicting features

**D. Clinical Decision Making:**
1. Recommended clinical pathway
2. When to escalate care
3. Follow-up plan
4. Patient education points

This assessment will be used to support professional medical decision-making and should reflect current best practices and evidence-based medicine.
"""
        return prompt
    
    @staticmethod
    def create_ai_prompt(complaint_id: int, prompt_type: str = 'combined') -> AIPrompt:
        """
        Create and save an AI prompt for a given complaint.
        
        Args:
            complaint_id: ID of the PatientComplaint
            prompt_type: Type of prompt ('triage', 'guidelines', or 'combined')
            
        Returns:
            AIPrompt instance
        """
        try:
            complaint = PatientComplaint.objects.get(id=complaint_id)
        except PatientComplaint.DoesNotExist:
            raise ValueError(f"PatientComplaint with id {complaint_id} does not exist")
        
        if prompt_type == 'triage':
            generated_prompt = PromptGenerator.generate_triage_prompt(complaint)
            triage_context = "Triage assessment for emergency/urgent care prioritization"
            guidelines_context = ""
        elif prompt_type == 'guidelines':
            generated_prompt = PromptGenerator.generate_guidelines_prompt(complaint)
            triage_context = ""
            guidelines_context = "Evidence-based clinical guidelines and protocols"
        else:  # combined
            generated_prompt = PromptGenerator.generate_combined_prompt(complaint)
            triage_context = "Comprehensive triage with urgency assessment"
            guidelines_context = "Evidence-based guidelines and best practices"
        
        ai_prompt = AIPrompt.objects.create(
            complaint=complaint,
            prompt_type=prompt_type,
            generated_prompt=generated_prompt,
            triage_context=triage_context,
            guidelines_context=guidelines_context
        )
        
        return ai_prompt
