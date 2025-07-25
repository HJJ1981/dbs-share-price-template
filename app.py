import os
import requests
import joblib
import sqlite3
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    name = request.form.get("q")
    if name:
        try:
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            # Insert the name with the current timestamp
            cursor.execute("INSERT INTO user (name, timestamp) VALUES (?, datetime('now'))", (name,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
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

@app.route("/telegram", methods=["GET", "POST"])
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
 
    return (render_template("telegram.html", status=status))

@app.route("/stop_telegram", methods=["GET", "POST"])
def stop_telegram():

    """Stop the Telegram bot by deleting the webhook."""
    domain_url = 'https://dbs-share-price-template-9kj1.onrender.com'

    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    webhook_response = requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is stopped. Please check with the telegram bot. @dsai_JJ_bot"
    else:
        status = "Failed to stop the telegram bot. Please check the logs."
    
    return(render_template("telegram.html", status=status))

@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    """This endpoint will be called by Telegram when a new message is received"""
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        # Extract the chat ID and message text from the update
        chat_id = update["message"]["chat"]["id"]
        query = update["message"]["text"]

        # Pass the query to the Groq model
        client = Groq()
        completion_ds = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        response_message = completion_ds.choices[0].message.content

        # Send the response back to the Telegram chat
        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(send_message_url, json={
            "chat_id": chat_id,
            "text": response_message
        })
    return('ok', 200)

@app.route('/sepia', methods=['GET', 'POST'])
def sepia():
    return render_template("sepia_hf.html")

@app.route("/user_log", methods=["GET", "POST"])
def user_log():
    """Display user logs from the database."""
    users = []
    try:
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        # Ensure the user table exists
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        conn.close()
    except sqlite3.Error:
        users = []
    return render_template("user_log.html", users=users)

@app.route("/delete_log", methods=["GET", "POST"])
def delete_log():
    """Delete all user logs from the database."""
    try:
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user")
        conn.commit()
        conn.close()
        status = "All user logs have been deleted."
    except sqlite3.Error as e:
        status = f"Error deleting logs: {e}"
    return render_template("delete_log.html", status=status)

if __name__ == "__main__":
    app.run()

# Set webhook for Telegram bot
# https://api.telegram.org/bot{groq_telegram_token}/setWebhook?url ={domain_url}/webhook

# Delete webhook for Telegram bot
# https: //api.telegram.org/bot%7Bgroq_telegram_token%7D/deleteWebhook

