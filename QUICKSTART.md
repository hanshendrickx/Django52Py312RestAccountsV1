# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
python manage.py migrate
```

### 3. Load Sample Data

```bash
python manage.py load_sample_data
```

This creates:
- Demo user: `demo_doctor` / `demo123`
- 3 sample patient complaints (P001, P002, P003)
- 3 AI prompts (one for each complaint)
- 2 prompt templates

### 4. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```

### 6. Access the Application

**Browsable API (Recommended for First-Time Users):**
1. Go to http://127.0.0.1:8000/api/scc/complaints/
2. Click "Log in" in the top right
3. Use credentials: `demo_doctor` / `demo123`
4. Browse the API and try creating complaints

**Admin Interface:**
1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser or use demo_doctor
3. Manage all data through Django admin

## Basic Workflow

### Creating a New Patient Complaint

1. Go to http://127.0.0.1:8000/api/scc/complaints/
2. Login if not already logged in
3. Fill in the form at the bottom:
   - Patient Identifier: `P004`
   - Chief Complaint: `Abdominal pain`
   - Signs & Symptoms: `Right upper quadrant pain, radiating to back`
   - History: `Started after fatty meal 6 hours ago`
   - Medical History: `Known gallstones, previous cholecystitis`
4. Click "POST"

### Generating an AI Prompt

1. After creating a complaint, note its ID (e.g., 4)
2. Go to http://127.0.0.1:8000/api/scc/complaints/4/generate_prompt/
3. Choose prompt type:
   - `triage` - For urgency assessment only
   - `guidelines` - For clinical guidelines only
   - `combined` - For comprehensive assessment (recommended)
4. Click "POST"

### Viewing Generated Prompts

1. Go to http://127.0.0.1:8000/api/scc/prompts/
2. See all prompts you've generated
3. Copy the `generated_prompt` text
4. Paste it into ChatGPT, Claude, or your preferred AI system

## Example Generated Prompt

When you generate a "combined" prompt for the chest pain case (P001), you get:

```markdown
# Professional Clinical Assessment - Grand Rounds Format

**Patient Case ID:** P001
**Chief Complaint:** Chest pain

**Subjective (S) - Signs & Current Complaints (SCC):**
Sharp chest pain radiating to left arm, diaphoresis, shortness of breath

**Professional Assessment Request (Pro-Prompt):**

Please provide:

**A. Triage Assessment:**
1. Urgency level (Critical/High/Medium/Low) with justification
2. Immediate management priorities
3. Red flags and concerning features

**B. Clinical Guidelines Review:**
1. Applicable evidence-based guidelines
2. Recommended diagnostic workup
3. Treatment protocols

**C. Differential Diagnosis:**
1. Most likely diagnoses (prioritized)
2. Must-not-miss diagnoses

**D. Clinical Decision Making:**
1. Recommended clinical pathway
2. Follow-up plan
```

This prompt is designed for professional medical use and follows Grand Rounds presentation format.

## Testing

Run the test suite:

```bash
python manage.py test
```

All 10 tests should pass:
- 3 model tests
- 6 prompt generation tests
- 1 template test

## What's Next?

1. **Customize Templates**: Create your own prompt templates in the admin
2. **Add More Cases**: Create complaints for different clinical scenarios
3. **Export Prompts**: Use the API to export prompts for case reviews
4. **Integrate with AI**: Use generated prompts with GPT-4, Claude, or other AI systems

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/scc/complaints/` | GET | List all complaints |
| `/api/scc/complaints/` | POST | Create new complaint |
| `/api/scc/complaints/{id}/` | GET | View complaint details |
| `/api/scc/complaints/{id}/generate_prompt/` | POST | Generate AI prompt |
| `/api/scc/prompts/` | GET | View generated prompts |
| `/api/scc/templates/` | GET | View prompt templates |

## Troubleshooting

**Can't login?**
- Make sure you ran `load_sample_data` to create the demo user
- Or create your own user with `createsuperuser`

**Server won't start?**
- Check if port 8000 is already in use
- Try: `python manage.py runserver 8001`

**Tests failing?**
- Make sure all migrations are applied: `python manage.py migrate`
- Check that you have all dependencies: `pip install -r requirements.txt`

## Need Help?

See the full documentation:
- README.md - Complete project documentation
- API_DOCS.md - Detailed API documentation
- examples/api_usage_example.py - Code examples

## Security Note

This is a development setup. For production:
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Configure proper database (PostgreSQL recommended)
- Set up proper authentication (OAuth, JWT, etc.)
- Enable HTTPS
- Configure CORS properly
- Set up proper logging and monitoring

## License

MIT License - Open Source
