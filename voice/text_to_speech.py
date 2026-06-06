import os
import subprocess
import re
from app.config import PIPER_PATH, MODEL_PATH, OUTPUT_FILE

def text_to_speech_piper(text):
    process = subprocess.run(
        [
            PIPER_PATH,
            "--model", MODEL_PATH,
            "--output_file", OUTPUT_FILE,
            "--length_scale", "1.2"
        ],
        input=text,
        text=True
    )

    os.system(f"start {OUTPUT_FILE}")


def humanize_text(text):
    
    text = re.sub(r"[*|#|-|_]", "", text)

    text = text.replace("\n", ". ")

    text = text.replace(",", ", ... ")
    
    text = text.replace(".", ". ... ")

    text = re.sub(r"\s+", " ", text).strip()

    return text