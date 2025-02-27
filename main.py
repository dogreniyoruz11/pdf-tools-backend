from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MERGED_FOLDER = "merged"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "PDF Tools Backend is Running!"

@app.route("/merge_pdfs", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    if not files or len(files) < 2:
        return {"error": "Please upload at least 2 PDFs"}, 400

    merger = PdfMerger()
    output_filename = os.path.join(MERGED_FOLDER, "merged_output.pdf")

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        merger.append(file_path)

    merger.write(output_filename)
    merger.close()

    return send_file(output_filename, as_attachment=True, download_name="merged.pdf")

if __name__ == "__main__":
    app.run(debug=True)
