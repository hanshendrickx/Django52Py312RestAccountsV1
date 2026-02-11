# API Documentation

## Overview

The SCC-AI Prompt Generator API provides endpoints for managing patient complaints and generating professional AI prompts for medical triage and clinical guidelines.

## Base URL

```
http://127.0.0.1:8000/api/
```

## Authentication

The API uses Django REST Framework's session authentication. You need to be logged in to access the endpoints.

### Login via Browsable API

Navigate to `http://127.0.0.1:8000/api/auth/login/` in your browser and log in.

### Login Programmatically

Use Django's session authentication by first logging in through the admin interface or creating a session.

## Endpoints

### 1. Patient Complaints

#### List Complaints
```http
GET /api/scc/complaints/
```

Returns all complaints created by the authenticated user.

**Response:**
```json
[
  {
    "id": 1,
    "created_by": 2,
    "created_by_username": "demo_doctor",
    "patient_identifier": "P001",
    "chief_complaint": "Chest pain",
    "signs_symptoms": "Sharp chest pain radiating to left arm...",
    "history_present_illness": "Sudden onset 2 hours ago...",
    "relevant_medical_history": "Hypertension, diabetes...",
    "created_at": "2026-02-11T13:52:00Z",
    "updated_at": "2026-02-11T13:52:00Z"
  }
]
```

#### Create Complaint
```http
POST /api/scc/complaints/
Content-Type: application/json
```

**Request Body:**
```json
{
  "patient_identifier": "P001",
  "chief_complaint": "Chest pain",
  "signs_symptoms": "Sharp chest pain radiating to left arm, diaphoresis",
  "history_present_illness": "Sudden onset 2 hours ago while at rest",
  "relevant_medical_history": "Hypertension, diabetes mellitus type 2"
}
```

**Response:** Returns the created complaint with `id` and timestamps.

#### Get Complaint
```http
GET /api/scc/complaints/{id}/
```

Returns details of a specific complaint.

#### Update Complaint
```http
PUT /api/scc/complaints/{id}/
PATCH /api/scc/complaints/{id}/
Content-Type: application/json
```

Use `PUT` for full update or `PATCH` for partial update.

#### Delete Complaint
```http
DELETE /api/scc/complaints/{id}/
```

Deletes the specified complaint and all associated AI prompts.

#### Generate AI Prompt
```http
POST /api/scc/complaints/{id}/generate_prompt/
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt_type": "combined"
}
```

**Prompt Types:**
- `triage` - Mock triage assessment only
- `guidelines` - Clinical guidelines consultation only
- `combined` - Comprehensive Pro-Prompt (default)

**Response:**
```json
{
  "id": 1,
  "complaint": 1,
  "complaint_summary": "P001 - Chest pain",
  "prompt_type": "combined",
  "generated_prompt": "# Professional Clinical Assessment - Grand Rounds Format\n\n**Patient Case ID:** P001\n...",
  "triage_context": "Comprehensive triage with urgency assessment",
  "guidelines_context": "Evidence-based guidelines and best practices",
  "created_at": "2026-02-11T13:52:00Z"
}
```

### 2. AI Prompts

#### List Prompts
```http
GET /api/scc/prompts/
```

Returns all AI prompts generated for the authenticated user's complaints.

#### Get Prompt
```http
GET /api/scc/prompts/{id}/
```

Returns details of a specific generated prompt.

### 3. Prompt Templates

#### List Templates
```http
GET /api/scc/templates/
```

Returns all active prompt templates available in the system.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Emergency Triage Template",
    "description": "Standard template for emergency department triage",
    "template_text": "Patient: {patient_identifier}\nChief Complaint: {chief_complaint}...",
    "is_active": true,
    "created_at": "2026-02-11T13:52:00Z",
    "updated_at": "2026-02-11T13:52:00Z"
  }
]
```

## Example Workflow

### 1. Create a Patient Complaint

Create a new complaint with patient's subjective information:

```bash
# Using the browsable API at http://127.0.0.1:8000/api/scc/complaints/
# Or programmatically after authentication
```

### 2. Generate AI Prompt

Once the complaint is created, generate an AI prompt:

```bash
# POST to /api/scc/complaints/{id}/generate_prompt/
# with body: {"prompt_type": "combined"}
```

### 3. Use the Generated Prompt

The generated prompt can be:
- Copied and pasted into AI systems (ChatGPT, Claude, etc.)
- Used for Grand Rounds presentations
- Shared with medical teams for discussion
- Stored for case review and documentation

### 4. Review AI Response

Medical professionals review the AI-generated assessment and make clinical decisions based on:
- Their professional judgment
- Current evidence-based guidelines
- Patient-specific factors
- Available resources

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

## Rate Limiting

Currently, no rate limiting is implemented. This is suitable for development and internal use.

## CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Modify `CORS_ALLOWED_ORIGINS` in settings.py for production use.

## Pagination

Currently, pagination is not enabled by default. All results are returned in a single response.

To enable pagination, add to `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Browsable API

Django REST Framework provides a browsable HTML interface for the API at:
- http://127.0.0.1:8000/api/scc/complaints/
- http://127.0.0.1:8000/api/scc/prompts/
- http://127.0.0.1:8000/api/scc/templates/

This interface allows you to:
- View available endpoints
- Test API calls directly from the browser
- See request/response formats
- Try different HTTP methods

## Admin Interface

Access the Django admin at http://127.0.0.1:8000/admin/ to:
- Manage users and permissions
- View and edit all data
- Create prompt templates
- Moderate content

Admin credentials:
- Username: `admin`
- Password: `admin123` (as created)

Or use demo credentials:
- Username: `demo_doctor`
- Password: `demo123`
