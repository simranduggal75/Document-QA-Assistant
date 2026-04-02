## 📄 Document Q&A Assistant

An end-to-end NLP-based web application that allows users to upload documents (PDF/TXT) and ask questions based on their content through an interactive UI.



## 🚀 Features

- 📤 Upload multiple documents (PDF, TXT)
- 📄 Automatic text extraction
- ✂️ Text chunking for efficient processing
- 🔍 Keyword-based search (information retrieval)
- 🤖 Answer extraction from relevant content
- 🌐 Interactive web interface (no Postman required)
- ⚡ AJAX-based upload and query (no page reload)



## 🧠 How It Works

1. Upload Documents
   Files are uploaded and stored locally.

2. Text Extraction
   Extracts content from PDF and TXT files using PyPDF2.

3. Chunking
   Splits large text into smaller chunks for better retrieval.

4. Search (Retrieval)
   Matches user query with chunks using keyword overlap.

5. Answer Extraction
   Selects the most relevant sentence as the final answer.



## 🛠️ Tech Stack

- Python
- Flask
- HTML / CSS
- JavaScript (Fetch API)
- PyPDF2
- Basic NLP (tokenization, keyword matching)



## 🔌 API Endpoints

## 1. Upload Documents

POST "/upload"

- Upload one or more PDF/TXT files
- Files are processed and stored locally

Request Type: "multipart/form-data"

Form Data:

- "files": one or multiple files

Response:

Uploaded: file1.pdf, file2.txt



## 2. Ask Question

POST "/ask"

- Takes a user query and returns an answer based on uploaded documents

Request Body (JSON):

{
  "query": "What are access modifiers?"
}

Response (JSON):

{
  "answer": "Access modifiers are keywords...",
  "source": "java1st.pdf"
}



## ⚠️ Limitations

- Uses keyword-based search (not semantic understanding)
- May return approximate results for vague queries
- Data stored in-memory (resets when server restarts)



## 🔮 Future Improvements

- Semantic search using embeddings
- Integration with LLMs (GPT / Gemini)
- Persistent storage (database / vector DB)
- Improved UI/UX



## 💡 Key Learning

Built a complete pipeline from document ingestion → text processing → retrieval → answer generation, similar to real-world RAG (Retrieval-Augmented Generation) systems.



## 👩‍💻 Author

Simran Duggal

AI/ML Engineer 


## ⭐ If you found this useful

Give this repo a ⭐ on GitHub!

## 📸 Output Screenshot
  Please refer to screenshots folder for output screenshots