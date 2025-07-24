from openai import OpenAI
from dotenv import load_dotenv
import os
import datetime
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def generate_ai_summary(transcript):

    date = datetime.datetime.now().strftime("%d/%m/%Y")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical assistant helping to document a medical record. You will be given a transcript of the conversation between the doctor and the patient. "
    "Please fill in the details for the following sections based on the patient's information, medical history, physical examination, and other relevant data.\n\n"
    
    """you'll also try to 3 give AI recommendations if possible based on the transcript. 
    AI-Diagnostic:  3 possible diagnostics by the AI discarding the doctor feedback
    So it will be like AI-Diagnostic 1 followed by AI-Treatment 1, AI-Diagnostic 2 followed by AI-Treatment 2
    AI-Treatment: suggest 3 treatments based on each diagnostic.
    if you can't make a recommendation leave this section out or type (I need more information for an AI recommendation) in the AI  reccomendation section\n\n"""

    "Leave out any data that is not mentioned. It's okay not to have all the info use `N/A` for missing info.\n\n"
f"""
    ## Patient Identification
- **Full Name:**  
- **Date of Birth:**  
- **Age:**  
- **Gender:**  
- **Patient ID:**  
- **Address:**  
- **Phone Number:**  
- **Emergency Contact:**  

---

## Chief Complaint 

---

## History of Present Illness (HPI)
  (Include onset, duration, severity, associated symptoms, alleviating/aggravating factors, etc.)

---

## Past Medical History (PMH)
- **Chronic Conditions:**  
- **Surgeries / Hospitalizations:**  
- **Allergies:**  
- **Medications:**  
- **Vaccination History:**  

---

## Family History (FH) 

---

## Social History (SH) 

---

## Review of Systems (ROS)

---

## Physical Examination
- **General Appearance:**  
- **Vital Signs (BP, HR, RR, Temp, O2 Sat):**  
- **Findings by System (HEENT, Chest, Abdomen, Neuro, Skin, etc.):**  

---

## Assessment / Doctor’s Impression
- **Doctor’s Observations and Feedback:**  
- **Preliminary Diagnosis:**  

---

## Plan / Treatment
- **Medications Prescribed:**  
- **Therapies / Procedures Suggested:**  
- **Follow-Up Instructions:**  

---

## Visit Details
- **Summary of Visit:**  
- **Tests / Procedures Conducted:**  
- **Date: {date}**  *(use {date} unless another date is mentioned in the transcript in form dd/mm/yyyy)*  
- **Results:**  
"""

    "---\n\n"

    "## AI Recommendation\n\n"

    "### AI-Diagnostic 1\n"
    "- **Possible Condition:**  \n"
    "- **Recommended Treatment:**  \n\n"
    "---\n\n"

    "### AI-Diagnostic 2\n"
    "- **Possible Condition:**  \n"
    "- **Recommended Treatment:**  \n\n"
    "---\n\n"

    "### AI-Diagnostic 3\n"
    "- **Possible Condition:**  \n"
    "- **Recommended Treatment:**  \n\n"

    "---\n\n"

    "Disregard any information not mentioned in the transcript."
    "Result is always in english"
                )
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )

    return response.choices[0].message.content.strip()