from flask import Flask, request, send_file, jsonify
import os
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder (using /tmp for Railway compatibility)
UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "✅ PDF Merger API is running!"})

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    if "files" not in request.files:
        return jsonify({"error": "No files provided. Please upload at least 2 PDFs."}), 400

    files = request.files.getlist("files")
    if len(files) < 2:
        return jsonify({"error": "Please upload at least 2 PDF files to merge."}), 400

    merger = PyPDF2.PdfMerger()
    file_paths = []

    try:
        for file in files:
            # Ensure the file is a PDF
            if not file.filename.lower().endswith(".pdf"):
                return jsonify({"error": f"Invalid file type: {file.filename}. Only PDF files are allowed."}), 400

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            file_paths.append(file_path)

            # Open file in binary mode to avoid EOF marker issues
            with open(file_path, "rb") as f:
                merger.append(f)

        # Output merged PDF file
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "merged.pdf")
        with open(output_path, "wb") as output_file:
            merger.write(output_file)

        merger.close()

        # Send merged PDF with correct headers
        return send_file(output_path, as_attachment=True, mimetype="application/pdf", download_name="merged.pdf")

    except PyPDF2.errors.PdfReadError:
        return jsonify({"error": "One or more PDF files are corrupted or not readable."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary files
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
