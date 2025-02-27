from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF Tools Backend is Running"

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    if 'files' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist("files")
    merger = PdfMerger()

    for file in files:
        merger.append(file)

    output_path = "merged.pdf"
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
