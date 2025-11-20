"""Generate demo CSV data for Monit Patient."""
import pandas as pd
import os
from datetime import datetime, timedelta
import random

# Create data directories
os.makedirs("data/patients", exist_ok=True)
os.makedirs("data/vitals", exist_ok=True)
os.makedirs("data/alerts", exist_ok=True)
os.makedirs("data/research/external_papers", exist_ok=True)
os.makedirs("data/research/internal_research", exist_ok=True)
os.makedirs("data/guidelines", exist_ok=True)
os.makedirs("data/agents", exist_ok=True)
os.makedirs("data/demo", exist_ok=True)

# Generate patient records
patients_data = [
    {
        "patient_id": "P001",
        "name": "John Doe",
        "age": 65,
        "gender": "male",
        "blood_type": "A+",
        "admission_date": "2025-01-10T08:30:00",
        "assigned_doctor": "Dr. Sarah Smith",
        "room_number": "ICU-201",
        "diagnosis": "Pneumonia",
        "medical_history": "Hypertension, Diabetes Type 2",
        "allergies": "Penicillin",
        "medications": "Metformin, Lisinopril",
        "emergency_contact": "+1-555-0101",
        "status": "active"
    },
    {
        "patient_id": "P002",
        "name": "Jane Smith",
        "age": 45,
        "gender": "female",
        "blood_type": "O-",
        "admission_date": "2025-01-12T14:20:00",
        "assigned_doctor": "Dr. James Wilson",
        "room_number": "ICU-202",
        "diagnosis": "Sepsis",
        "medical_history": "None",
        "allergies": "None",
        "medications": "Antibiotics, IV fluids",
        "emergency_contact": "+1-555-0102",
        "status": "critical"
    },
    {
        "patient_id": "P003",
        "name": "Robert Johnson",
        "age": 72,
        "gender": "male",
        "blood_type": "B+",
        "admission_date": "2025-01-13T10:15:00",
        "assigned_doctor": "Dr. Sarah Smith",
        "room_number": "ICU-203",
        "diagnosis": "Cardiac Arrest",
        "medical_history": "CAD, Previous MI",
        "allergies": "Aspirin",
        "medications": "Anticoagulants, Beta-blockers",
        "emergency_contact": "+1-555-0103",
        "status": "active"
    }
]

patients_df = pd.DataFrame(patients_data)
patients_df.to_csv("data/patients/patient_records.csv", index=False)
print("✓ Generated patient_records.csv")

# Generate vitals history
vitals_data = []
base_time = datetime.utcnow() - timedelta(hours=24)

for patient in patients_data:
    patient_id = patient["patient_id"]

    # Generate 50 vitals records for each patient
    for i in range(50):
        timestamp = base_time + timedelta(minutes=i*30)

        # Base vitals with some variation
        if patient_id == "P001":  # Stable with slight variations
            heart_rate = random.randint(70, 90)
            bp_sys = random.randint(115, 135)
            bp_dia = random.randint(75, 85)
            o2_sat = random.uniform(96, 99)
            temp = random.uniform(36.8, 37.5)
        elif patient_id == "P002":  # Critical - sepsis patterns
            heart_rate = random.randint(100, 130)
            bp_sys = random.randint(85, 110)
            bp_dia = random.randint(50, 70)
            o2_sat = random.uniform(90, 95)
            temp = random.uniform(38.0, 39.5)
        else:  # P003 - Cardiac issues
            heart_rate = random.randint(55, 75)
            bp_sys = random.randint(90, 120)
            bp_dia = random.randint(60, 80)
            o2_sat = random.uniform(94, 97)
            temp = random.uniform(36.5, 37.2)

        vitals_data.append({
            "patient_id": patient_id,
            "heart_rate": heart_rate,
            "bp_systolic": bp_sys,
            "bp_diastolic": bp_dia,
            "o2_saturation": round(o2_sat, 1),
            "temperature": round(temp, 1),
            "respiratory_rate": random.randint(12, 20),
            "timestamp": timestamp.isoformat()
        })

vitals_df = pd.DataFrame(vitals_data)
vitals_df.to_csv("data/vitals/vitals_history.csv", index=False)
print("✓ Generated vitals_history.csv")

# Generate medical guidelines
guidelines_data = [
    {
        "guideline_id": "G001",
        "category": "Sepsis",
        "title": "Early Sepsis Recognition",
        "description": "Identify sepsis within first hour using qSOFA criteria",
        "criteria": "2 or more: RR>=22, altered mentation, SBP<=100mmHg",
        "action": "Start broad-spectrum antibiotics within 1 hour"
    },
    {
        "guideline_id": "G002",
        "category": "Cardiac",
        "title": "Acute MI Management",
        "description": "STEMI identification and rapid intervention",
        "criteria": "ST elevation in 2+ contiguous leads",
        "action": "Activate cath lab, aspirin, anticoagulation"
    },
    {
        "guideline_id": "G003",
        "category": "Respiratory",
        "title": "Hypoxemia Protocol",
        "description": "Management of low oxygen saturation",
        "criteria": "SpO2 < 92%",
        "action": "Supplemental oxygen, assess for respiratory failure"
    }
]

guidelines_df = pd.DataFrame(guidelines_data)
guidelines_df.to_csv("data/guidelines/medical_guidelines.csv", index=False)
print("✓ Generated medical_guidelines.csv")

# Generate emergency protocols
protocols_data = [
    {
        "protocol_id": "EP001",
        "name": "Code Blue",
        "trigger": "Cardiac arrest",
        "steps": "Call code, start CPR, prepare defibrillator"
    },
    {
        "protocol_id": "EP002",
        "name": "Rapid Response",
        "trigger": "Deteriorating patient",
        "steps": "Assess ABC, call team, stabilize"
    }
]

protocols_df = pd.DataFrame(protocols_data)
protocols_df.to_csv("data/guidelines/emergency_protocols.csv", index=False)
print("✓ Generated emergency_protocols.csv")

# Generate research papers summaries
research_data = [
    {
        "paper_id": "R001",
        "title": "Early Detection of Sepsis Using Machine Learning",
        "authors": "Smith et al.",
        "year": 2023,
        "journal": "JAMA",
        "key_findings": "ML models can predict sepsis 4-6 hours before clinical diagnosis",
        "relevance": "high"
    },
    {
        "paper_id": "R002",
        "title": "Vital Signs Trajectories in ICU Patients",
        "authors": "Johnson et al.",
        "year": 2024,
        "journal": "Critical Care Medicine",
        "key_findings": "Declining oxygen saturation predicts deterioration with 85% accuracy",
        "relevance": "high"
    }
]

research_df = pd.DataFrame(research_data)
research_df.to_csv("data/research/external_papers/sepsis_studies.csv", index=False)
print("✓ Generated sepsis_studies.csv")

# Generate internal case studies
case_studies_data = [
    {
        "case_id": "CS001",
        "patient_demographics": "Male, 68, hypertensive",
        "presenting_symptoms": "Fever, hypotension, tachycardia",
        "diagnosis": "Septic shock",
        "treatment": "Broad-spectrum antibiotics, fluid resuscitation",
        "outcome": "Recovered",
        "lessons_learned": "Early antibiotic administration crucial"
    }
]

case_studies_df = pd.DataFrame(case_studies_data)
case_studies_df.to_csv("data/research/internal_research/case_studies.csv", index=False)
print("✓ Generated case_studies.csv")

# Generate agent configurations placeholder
agent_configs_data = [
    {
        "config_id": "default",
        "name": "Default Configuration",
        "config_json": "{}",
        "created_at": datetime.utcnow().isoformat()
    }
]

agent_configs_df = pd.DataFrame(agent_configs_data)
agent_configs_df.to_csv("data/agents/agent_configurations.csv", index=False)
print("✓ Generated agent_configurations.csv")

# Create empty files for other data
pd.DataFrame(columns=["alert_id", "patient_id", "alert_type", "severity", "message", "timestamp", "status"]).to_csv("data/alerts/alert_history.csv", index=False)
print("✓ Generated alert_history.csv")

pd.DataFrame().to_csv("data/guidelines/drug_interactions.csv", index=False)
print("✓ Generated drug_interactions.csv")

pd.DataFrame().to_csv("data/research/internal_research/treatment_outcomes.csv", index=False)
print("✓ Generated treatment_outcomes.csv")

pd.DataFrame().to_csv("data/research/external_papers/cardiac_studies.csv", index=False)
print("✓ Generated cardiac_studies.csv")

pd.DataFrame().to_csv("data/research/external_papers/respiratory_studies.csv", index=False)
print("✓ Generated respiratory_studies.csv")

pd.DataFrame().to_csv("data/agents/agent_performance_logs.csv", index=False)
print("✓ Generated agent_performance_logs.csv")

print("\n✅ All demo data generated successfully!")
print(f"   - {len(patients_data)} patients")
print(f"   - {len(vitals_data)} vital sign records")
print(f"   - {len(guidelines_data)} medical guidelines")
print(f"   - {len(research_data)} research papers")
