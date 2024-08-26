from flask import Flask, render_template, request, flash
from main import Exicute
import datetime
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Validate username and password
        if not username or not password:
            flash("Username and password are required!")
            return render_template("index.html")

        # Collect the classes from the form inputs
        classes = []
        for i in range(1, 7):
            class_crn = request.form.get(f"class{i}")
            if class_crn:
                classes.append(class_crn)

        hour = int(request.form["hour"])
        minute = int(request.form["minute"])
        ampm = request.form["ampm"]

        # Convert to 24-hour format
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        execute_time = f"{hour:02d}:{minute:02d}:00"

        # Validate the execution time
        now = datetime.datetime.now()
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target_time <= now:
            flash("The specified time has already passed. Please select a future time.")
            return render_template("index.html")

        # Flash a waiting message
        flash("Bot is waiting for the scheduled time...")

        # Simulate waiting time for user to see the message
        time.sleep(2)

        # Run the bot
        try:
            flash("Bot is starting...")
            message = Exicute(password, username, classes, execute_time)
            flash(message)
        except Exception as e:
            flash("An error occurred. Please ensure you have a strong Wi-Fi connection and try again.")

        return render_template("index.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
