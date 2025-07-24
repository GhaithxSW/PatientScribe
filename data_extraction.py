from openai import OpenAI
import json

client = OpenAI()

def extract_patient_data(transcript):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that extracts medical information from transcripts "
                    "and returns a flat JSON object with exactly these keys: "
                    "`name`, `symptoms`, `diagnosis`, `chronicConditions`, `surgeries`, and `allergies`.\n\n"
                    "Rules:\n"
                    "- Use plain strings only, no markdown, no triple backticks.\n"
                    "- If any field is missing, use default values like 'N/A', 'None', or 'No known allergies'.\n"
                    "- Do NOT return anything other than the JSON object.\n"
                )
            },
            {
                "role": "user",
                "content": f"Extract patient data from the following transcript:\n\n{transcript}"
            }
        ]
    )

    extracted_data = response.choices[0].message.content.strip()
    print(f"Extracted Data: {extracted_data}")

    # Parse JSON
    try:
        data = json.loads(extracted_data)
        return data
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        return {
            "name": "N/A",
            "symptoms": "N/A",
            "diagnosis": "N/A",
            "chronicConditions": "N/A",
            "surgeries": "N/A",
            "allergies": "N/A"
        }
