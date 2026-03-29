from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Doc QA Assistant Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)