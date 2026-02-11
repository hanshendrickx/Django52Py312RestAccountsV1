# Django 5.2 SCC-AI Prompt Generator

A Django 5.2 REST API application for generating AI prompts from patient Signs & Current Complaints (SCC). This project combines REST API functionality with a medical consultation workflow based on the SOAP methodology, specifically focusing on the Subjective (S) component.

## Project Overview

This is an Open Source project (MIT License) by Hans Hendrickx MD PhD. The goal is to create an SCC (Signs & Current Complaints) AI prompt generator for patients that combines:

- **"S" (Subjective) part**: Patient-reported signs and symptoms
- **"Pro"-prompt**: Professional-level prompts suitable for Grand Rounds meetings

The combined prompts can be used to trigger AI for:
- **Mock Triage**: Urgency assessment and immediate care prioritization
- **Mock Guidelines**: Evidence-based clinical guideline recommendations

These AI-generated assessments are designed to be further objectivated by medical professionals.

## Features

- ✅ Django 5.2 with Python 3.12
- ✅ Django REST Framework for API endpoints
- ✅ Custom user authentication system
- ✅ Patient complaint management (Signs & Current Complaints)
- ✅ AI prompt generation for triage and clinical guidelines
- ✅ Professional-level prompts for Grand Rounds format
- ✅ REST API with full CRUD operations
- ✅ Django Admin interface for data management

## Installation

### Prerequisites

- Python 3.12
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hanshendrickx/Django52Py312RestAccountsV1.git
cd Django52Py312RestAccountsV1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `GET/POST /api/auth/login/` - Login (session-based)
- `GET/POST /api/auth/logout/` - Logout

### Patient Complaints (SCC)
- `GET /api/scc/complaints/` - List all complaints (user's own)
- `POST /api/scc/complaints/` - Create a new complaint
- `GET /api/scc/complaints/{id}/` - Get a specific complaint
- `PUT/PATCH /api/scc/complaints/{id}/` - Update a complaint
- `DELETE /api/scc/complaints/{id}/` - Delete a complaint
- `POST /api/scc/complaints/{id}/generate_prompt/` - Generate AI prompt for a complaint

### AI Prompts
- `GET /api/scc/prompts/` - List all generated prompts (user's own)
- `GET /api/scc/prompts/{id}/` - Get a specific prompt

### Prompt Templates
- `GET /api/scc/templates/` - List available prompt templates

## Usage Examples

### Creating a Patient Complaint

```bash
curl -X POST http://127.0.0.1:8000/api/scc/complaints/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "patient_identifier": "P001",
    "chief_complaint": "Chest pain",
    "signs_symptoms": "Sharp chest pain radiating to left arm, started 2 hours ago",
    "history_present_illness": "Patient reports sudden onset while at rest",
    "relevant_medical_history": "Hypertension, diabetes, smoker"
  }'
```

### Generating an AI Prompt

```bash
curl -X POST http://127.0.0.1:8000/api/scc/complaints/1/generate_prompt/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "prompt_type": "combined"
  }'
```

Available prompt types:
- `triage` - Mock triage assessment only
- `guidelines` - Clinical guidelines only
- `combined` - Comprehensive Pro-Prompt (default)

### Example Generated Prompt

When you generate a "combined" prompt, you'll receive a professionally formatted prompt like:

```
# Professional Clinical Assessment - Grand Rounds Format

**Patient Case ID:** P001

**Chief Complaint:** Chest pain

**Subjective (S) - Signs & Current Complaints (SCC):**
Sharp chest pain radiating to left arm, started 2 hours ago

**History of Present Illness:**
Patient reports sudden onset while at rest

**Relevant Medical History:**
Hypertension, diabetes, smoker

**Professional Assessment Request (Pro-Prompt):**

This case is presented for comprehensive clinical evaluation combining both 
triage and guidelines review, as would be conducted in a Grand Rounds setting.

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

[... continues with detailed professional assessment framework ...]
```

## Data Models

### PatientComplaint
Stores patient Signs & Current Complaints (S from SOAP):
- `patient_identifier` - Patient ID or case number
- `chief_complaint` - Main complaint
- `signs_symptoms` - Detailed signs and symptoms
- `history_present_illness` - HPI
- `relevant_medical_history` - Relevant PMH

### AIPrompt
Stores generated AI prompts:
- `complaint` - Reference to PatientComplaint
- `prompt_type` - Type: triage, guidelines, or combined
- `generated_prompt` - The AI-ready prompt text
- `triage_context` - Triage-specific context
- `guidelines_context` - Guidelines-specific context

### PromptTemplate
Reusable templates for prompt generation:
- `name` - Template name
- `description` - Template description
- `template_text` - Template with placeholders

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` to:
- Manage users
- View and edit patient complaints
- Review generated AI prompts
- Manage prompt templates

## Testing

Run the test suite:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test scc_prompts
```

## Development

This project uses:
- Django 5.2
- Django REST Framework 3.15
- django-cors-headers for CORS support
- SQLite database (default, suitable for development)

## License

MIT License - Open Source

## Author

Hans Hendrickx MD PhD

## Acknowledgments

Based on REST and Accounts work by William Vincent, with significant adjustments for medical consultation workflows.

## Contributing

Contributions are welcome! This is an open-source project designed to support medical professionals in generating structured AI prompts for clinical decision support.

## Disclaimer

This tool is designed to assist medical professionals in structuring patient information for AI-assisted triage and guideline review. All AI-generated content must be reviewed and validated by qualified medical professionals. This tool does not replace professional medical judgment.
