from flask import Flask, request, send_file, jsonify
import os
import PyPDF2
from werkzeug.utils import secure_filename
from flask_cors import CORS  # 🔥 Enable CORS

app = Flask(__name__)
CORS(app)  # 🔥 Allow all origins

UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "✅ PDF Merger API is running!"})

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    if "files" not in request.files:
        return jsonify({"error": "No files found. Please upload at least 2 PDFs."}), 400

    files = request.files.getlist("files")
    if len(files) < 2:
        return jsonify({"error": "At least 2 PDF files required."}), 400

    merger = PyPDF2.PdfMerger()
    file_paths = []

    try:
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            file_paths.append(file_path)
            merger.append(file_path)

        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "merged.pdf")
        merger.write(output_path)
        merger.close()

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
