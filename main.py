import os
import io
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Local imports
from summarizer import generate_ai_summary
from transcription import transcribe_audio
from data_extraction import extract_patient_data

app = FastAPI()

# ---------------------------------------------------------
# ✅ CORS Configuration (allow frontend to call backend)
# ---------------------------------------------------------
origins = [
    "http://localhost:3000"
    "https://victorious-plant-0d66aff1e.6.azurestaticapps.net",
    "http://localhost",
    "http://localhost:8080",
    "https://mediscribeai.azurewebsites.net",
    "https://mediscribe.elev8xr.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 🩺 Health Check Route
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "✅ FastAPI backend is running."}

# ---------------------------------------------------------
# 🎤 Upload Audio, Transcribe, Extract Info
# ---------------------------------------------------------
@app.post("/upload/")
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # Save original audio
        raw_path = os.path.join(upload_dir, file.filename)
        with open(raw_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert and standardize audio format
        processed_path = os.path.join(upload_dir, f"processed_{file.filename}")
        audio = AudioSegment.from_file(raw_path)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        audio.export(processed_path, format="wav")

        # Run transcription and data extraction
        with open(processed_path, "rb") as audio_file:
            transcript = transcribe_audio(audio_file)

        patient_data = extract_patient_data(transcript)
        summary = generate_ai_summary(transcript)

        return JSONResponse(content={
            "transcript": transcript,
            "patient_data": patient_data,
            "summary": summary
        })

    except Exception as e:
        print(f"Error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# ---------------------------------------------------------
# 📄 Generate PDF Report
# ---------------------------------------------------------
@app.post("/generate-pdf/")
async def generate_pdf(request: Request):
    try:
        data = await request.json()

        def get(key, default="N/A"):
            return data.get(key, default)

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 40

        def draw_section(title, items):
            nonlocal y
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(40, y, title)
            y -= 20
            pdf.setFont("Helvetica", 12)
            for label, value in items:
                pdf.drawString(60, y, f"{label}: {value}")
                y -= 18
            y -= 10

        # PDF Header
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(width / 2, y, "Pediatric Medical Record")
        y -= 40
        pdf.setFont("Helvetica", 12)
        pdf.drawString(40, y, f"Prepared by: {get('prepared_by', 'AI Assistant')}")
        y -= 30

        draw_section("Patient Information", [
            ("Full Name", get("name")),
            ("Date of Birth", get("dob")),
            ("Age", get("age")),
            ("Gender", get("gender")),
            ("Patient ID", get("id")),
            ("Address", get("address")),
            ("Phone Number", get("phone")),
            ("Emergency Contact", get("emergency_contact")),
            ("Primary Care Physician", get("doctor")),
        ])

        draw_section("Medical History", [
            ("Chronic Conditions", get("chronicConditions")),
            ("Surgeries/Hospitalizations", get("surgeries")),
            ("Allergies", get("allergies")),
        ])

        draw_section("Assessment and Plan", [
            ("Primary Diagnosis", get("diagnosis")),
            ("Treatment", get("treatment")),
            ("Follow-up", get("follow_up")),
        ])

        pdf.showPage()
        pdf.save()
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="application/pdf", headers={
            "Content-Disposition": "inline; filename=medical_record.pdf"
        })

    except Exception as e:
        print(f"PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="PDF generation failed.")
