from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files' not in request.files:
        return {"error": "No files part in the request"}, 400

    files = request.files.getlist('files')
    
    if not files or len(files) < 2:
        return {"error": "Please upload at least 2 PDF files"}, 400

    merger = PdfMerger()

    for file in files:
        if file.filename == '':
            return {"error": "One or more files have no filename"}, 400
        merger.append(file)

    output_filename = "merged.pdf"
    merger.write(output_filename)
    merger.close()

    return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
