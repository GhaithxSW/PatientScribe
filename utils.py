import os

def save_audio_file(file, file_location):
    """Save the uploaded audio file to the specified location."""
    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise Exception(f"Error saving file: {str(e)}")
