from flask import Flask, render_template, request
import joblib
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    q = request.form.get("q")
    # You can use `q` for database logic here
    return render_template("main.html")

@app.route("/llama", methods=["GET", "POST"])
def llama():
    return render_template("llama.html")

@app.route("/llama_reply", methods=["GET", "POST"])
def llama_reply():
    q = request.form.get("q")

    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": q}
        ]
    )
    return render_template("llama_reply.html", r=completion.choices[0].message.content)

@app.route("/deepseek", methods=["GET", "POST"])
def deepseek():
    return render_template("deepseek.html")

@app.route("/deepseek_reply", methods=["GET", "POST"])
def deepseek_reply():
    q = request.form.get("q")

    client = Groq(api_key=GROQ_API_KEY)
    completion_ds = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "user", "content": q}
        ]
    )
    return render_template("deepseek_reply.html", r=completion_ds.choices[0].message.content)

@app.route("/dbs", methods=["GET", "POST"])
def dbs():
    return render_template("dbs.html")

@app.route("/prediction", methods=["POST"])
def prediction():
    q = float(request.form.get("q"))
    result = round(-50.6 * q + 90.2, 2)
    return render_template("prediction.html", r=result)

@app.route("/telgram", methods=["GET", "POST"])
def telegram():
    domain_url = 'https://dbs-share-price-template-9kj1.onrender.com'

    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    # The following line is used to set the webhook URL for the Telegram bot
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={domain_url}/webhook"
    webhook_response = requests.post(set_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is running. Please check with the telegram bot. @dsai_JJ_bot"
    else:
        status = "Failed to start the telegram bot. Please check the logs."
 
    return (render_template("telgram.html", status=status))

if __name__ == "__main__":
    app.run(debug=True)

