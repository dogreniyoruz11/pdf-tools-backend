from flask import Flask, request, send_file, jsonify
import PyPDF2
import os

app = Flask(__name__)

# Merge PDF Route
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    try:
        pdf_files = request.files.getlist('files')
        if not pdf_files:
            return jsonify({"error": "No files uploaded"}), 400
        
        merger = PyPDF2.PdfMerger()
        for pdf in pdf_files:
            merger.append(pdf)

        output_filename = "merged.pdf"
        merger.write(output_filename)
        merger.close()

        return send_file(output_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home Route to check if API is running
@app.route("/", methods=["GET"])
def home():
    return "Backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
