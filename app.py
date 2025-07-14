from flask import Flask, render_template, request
import joblib
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("API_KEY")
# for cloud............

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    q = request.form.get("q")
    # db
    return render_template("main.html")

@app.route("/llama", methods=["GET", "POST"])
def llama():
    return render_template("llama.html")

@app.route("/llama_reply", methods=["GET", "POST"])
def llama_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": q
            }
        ]
    )
    return(render_template("llama_reply.html",r=completion.choices[0].message.content))

@app.route("/dbs", methods=["GET", "POST"])
def dbs():
    return render_template("dbs.html")

@app.route("/prediction", methods=["POST"])
def prediction():
    q = float(request.form.get("q"))
    result = round(-50.6 * q + 90.2, 2)
    return render_template("prediction.html", r=result)

if __name__ == "__main__":
    app.run(debug=True)
