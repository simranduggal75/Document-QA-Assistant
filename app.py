from flask import Flask , render_template , request , jsonify
import os
import re

document_chunks = []
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
    
    
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start += chunk_size - overlap

    return chunks
    
def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def find_best_chunks(query, top_k=3):
    query_tokens = set(tokenize(query))
    scores = []

    for chunk in document_chunks:
        chunk_tokens = set(tokenize(chunk["text"]))
        score = len(query_tokens & chunk_tokens)  

        scores.append((score, chunk))

    scores.sort(key=lambda x : x[0],reverse=True)

    return [chunk for score, chunk in scores[:top_k] if score > 0]

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
        
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        document_chunks.append({
        "text": chunk,
        "source": file.filename,
        "chunk_id": i
    })

    print(f"📦 {file.filename} split into {len(chunks)} chunks")

    return f"Uploaded: {', '.join(saved_files)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query"})

    if not document_chunks:
        return jsonify({"error": "No documents uploaded"})

    results = find_best_chunks(query)

    if not results:
        return jsonify({"answer": "No relevant information found."})

    return jsonify({
        "answer": results[0]["text"][:300],
        "top_chunks": results
    })

if __name__ == "__main__":
    app.run(debug=True)