#!/usr/bin/env python3
"""
Example script demonstrating how to use the SCC-AI Prompt Generator API.
"""

import json

def example_create_complaint():
    complaint_data = {
        "patient_identifier": "P999",
        "chief_complaint": "Severe headache",
        "signs_symptoms": "Sudden onset worst headache of life",
    }
    
    print("=" * 70)
    print("EXAMPLE: Creating a Patient Complaint")
    print("=" * 70)
    print("\nRequest Data:")
    print(json.dumps(complaint_data, indent=2))

def main():
    print("\nSCC-AI Prompt Generator - API Usage Examples")
    example_create_complaint()

if __name__ == "__main__":
    main()
