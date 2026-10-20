from flask import Flask, render_template, request, redirect, session
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = "secret123"

print("🚀 Starting Flask Server...")


# ================= DATABASE =================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Narmatha@123",
    database="diet_system"
)

cursor = db.cursor(dictionary=True, buffered=True)


# ================= PASSWORD VALIDATION =================

def valid_password(password):

    if len(password) < 8:
        return False
    if not re.search("[@#$%^&+=]", password):
        return False

    return True


# ================= DISEASE MAPPING =================

def map_disease(disease):

    if disease in [
        "Diabetes",
        "Hypertension",
        "High BP",
        "Cholesterol"
    ]:
        return "Diabetes"

    elif disease in [
        "Obesity",
        "Weight Loss",
        "Low Immunity",
        "Vitamin Deficiency"
    ]:
        return "Obesity"

    elif disease == "Weight Gain":
        return "Weight Gain"

    elif disease in [
        "Kidney Disease",
        "Liver Disease",
        "Digestive Issues",
        "Ulcer"
    ]:
        return "Kidney Disease"

    else:
        return "General"


# ================= LOGIN =================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        query = """
        SELECT * FROM users
        WHERE username=%s AND password=%s
        """

        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:

            session["user"] = username
            session["user_id"] = user["id"]   # ⭐ IMPORTANT

            if user["role"] == "admin":
                return redirect("/admin")

            return redirect("/home")

        else:
            return "Invalid Login"

    return render_template("login.html")


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if not valid_password(password):
            return "Password must be 8 characters with symbol"

        query = """
        INSERT INTO users
        (username,password,role)
        VALUES (%s,%s,'user')
        """

        cursor.execute(query, (username, password))
        db.commit()

        return redirect("/")

    return render_template("register.html")


# ================= HOME =================

@app.route("/home", methods=["GET", "POST"])
def home():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"]
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        disease = request.form["disease"]
        decision = request.form["decision"]

        # ⭐ ADD THIS
        plan_type = request.form["plan_type"]

        # ===== BMI =====

        bmi = weight / ((height/100) ** 2)

        # ===== WATER =====

        water_intake = round(weight * 0.033, 2)

        # ===== MAP DISEASE =====

        mapped_disease = map_disease(disease)

        # ===== WEEKLY DIET =====

        cursor.execute(
            "SELECT * FROM weekly_diet WHERE disease=%s",
            (mapped_disease,)
        )

        weekly_data = cursor.fetchall()

        if not weekly_data:

            cursor.execute(
                "SELECT * FROM weekly_diet WHERE disease='General'"
            )

            weekly_data = cursor.fetchall()

        # ===== PLAN TYPE LOGIC =====

        month_data = []
        day_data = []

        if plan_type == "day":
            day_data = []
            if weekly_data:
                first_day = weekly_data[0]
                day_data = [
                    {"meal": "Breakfast", "food": 
        first_day["breakfast"]},
                    {"meal": "Lunch", "food":
        first_day["lunch"]},
                    {"meal": "Dinner", "food":
        first_day["dinner"]},
                    {"meal": "Snack", "food":
        first_day.get("snack", "Healthy Fruits")}
                ]
            

        elif plan_type == "week":
            pass


        elif plan_type == "month":

            for i in range(4):
                month_data.append(weekly_data)

        # ===== SUGGESTIONS =====

        cursor.execute(
            "SELECT * FROM suggestions WHERE disease=%s",
            (mapped_disease,)
        )

        suggestion = cursor.fetchone()

        if not suggestion:

            cursor.execute(
                "SELECT * FROM suggestions WHERE disease='General'"
            )

            suggestion = cursor.fetchone()

        # ===== SAVE USER INPUT =====

        insert_query = """
        INSERT INTO user_inputs
        (name,age,height,weight,
        disease,decision,bmi)

        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            insert_query,
            (name, age, height,
             weight, disease,
             decision, bmi)
        )

        db.commit()

        # ===== SAVE DIET REQUEST =====

        cursor.execute("""
        INSERT INTO diet_requests
        (user_id, disease)
        VALUES (%s,%s)
        """,
        (session["user_id"], mapped_disease)
        )

        db.commit()

        # ===== REPORT =====

        if bmi < 18.5:

            report = "You are underweight. Focus on high-calorie foods."

        elif bmi < 25:

            report = "You have normal BMI. Maintain balanced diet."

        else:

            report = "You are overweight. Follow low-calorie diet."

        report += f" Diet plan created for {mapped_disease}."
        report += f" Goal: {decision}."

        # ⭐ CORRECT RETURN (INSIDE FUNCTION)

        return render_template(
            "result.html",
            name=name,
            disease=disease,
            decision=decision,
            bmi=round(bmi, 2),
            weekly_data=weekly_data,
            month_data=month_data,
            day_data=day_data,
            plan_type=plan_type,
            suggestion=suggestion,
            report=report,
            water_intake=water_intake
        )

    return render_template("home.html")



# ================= ADMIN DASHBOARD =================

@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/")

    cursor.execute(
        "SELECT * FROM user_inputs ORDER BY id ASC"
    )

    data = cursor.fetchall()

    # ===== COUNTS =====

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM user_inputs")
    total_reports = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM messages")
    total_messages = cursor.fetchone()["total"]

    # ⭐ NEW COUNT

    cursor.execute("SELECT COUNT(*) AS total FROM diet_requests")
    total_diet_requests = cursor.fetchone()["total"]

    return render_template(
        "admin.html",
        data=data,
        total_users=total_users,
        total_reports=total_reports,
        total_messages=total_messages,
        total_diet_requests=total_diet_requests
    )


# ================= USER MESSAGE =================

@app.route('/send_message', methods=['POST'])
def send_message():

    sender = request.form['sender']
    message = request.form['message']

    query = """
    INSERT INTO messages
    (sender, receiver, message)
    VALUES (%s,%s,%s)
    """

    cursor.execute(
        query,
        (sender, "Admin", message)
    )

    db.commit()

    return redirect("/home")


# ================= ADMIN MESSAGES =================

@app.route('/admin_messages')
def admin_messages():

    cursor.execute(
        "SELECT * FROM messages ORDER BY id ASC"
    )

    messages = cursor.fetchall()

    return render_template(
        'admin_messages.html',
        messages=messages
    )


# ================= ADMIN REPLY =================

@app.route('/reply/<int:id>', methods=['POST'])
def reply(id):

    reply_text = request.form['reply']

    query = """
    UPDATE messages
    SET reply=%s
    WHERE id=%s
    """

    cursor.execute(query, (reply_text, id))

    db.commit()

    return redirect('/admin_messages')


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("user", None)
    session.pop("user_id", None)

    return redirect("/")


# ================= RUN =================

if __name__ == "__main__":

    app.run(debug=True)