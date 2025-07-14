from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    q = (request.form.get("q"))
    # db
    return (render_template("main.html"))

@app.route("/main", methods=["GET", "POST"])
def dbs():
    return (render_template("dbs.html"))

@app.route("/prediction", methods=["POST"])
def prediction():
    q = float(request.form.get("q"))
    result = round(-50.6 * q + 90.2, 2)
    return render_template("prediction.html", r=result)

if __name__ == "__main__":
    app.run(debug=True)

