from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # ضروري للرسائل المؤقتة

# --- إعداد MongoDB ---
MONGO_URI = os.getenv("MONGO_URI")  # ضع رابط MongoDB الخاص بك في Render كـ environment variable
client = MongoClient(MONGO_URI)
db = client["orthopedics_db"]
messages_collection = db["messages"]

# --- الصفحة الرئيسية ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if name and email and message:
            messages_collection.insert_one({
                "name": name,
                "email": email,
                "message": message
            })
            flash("تم إرسال رسالتك بنجاح!", "success")
            return redirect(url_for("index"))
        else:
            flash("يرجى ملء جميع الحقول.", "error")
            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
