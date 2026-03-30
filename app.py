from flask import Flask , render_template , request , jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_pdf(filepath):
    try:
        import PyPDF2
        text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")

    if not files or all(f.filename == "" for f in files):
        return "No files selected"

    saved_files = []

    for file in files:
        if file.filename == "":
            continue

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Detect file type
        ext = os.path.splitext(file.filename)[1].lower()

        if ext == ".txt":
            text = extract_text_from_txt(filepath)
        elif ext == ".pdf":
            text = extract_text_from_pdf(filepath)
        else:
            text = "Unsupported file type"

        print(f"\n📄 Extracted from {file.filename}:\n{text[:200]}...\n")
        saved_files.append(file.filename)

    return f"Uploaded: {', '.join(saved_files)}"

if __name__ == "__main__":
    app.run(debug=True)