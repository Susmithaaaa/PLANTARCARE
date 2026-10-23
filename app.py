
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file
)

import os
import joblib
import pandas as pd

from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "plantarcare-local-key"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_FILE = os.path.join(
    BASE_DIR,
    "plantarcare_model.pkl"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(REPORT_FOLDER, exist_ok=True)


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

model = None

try:
    package = joblib.load(MODEL_FILE)

    if isinstance(package, dict):
        model = package.get("model")
    else:
        model = package

    if model is not None:
        print("PLANTARCARE model loaded successfully.")
    else:
        print("Model file loaded, but no model object was found.")

except Exception as error:
    print("Model loading error:", error)
    model = None


# ============================================================
# VIDEO LIBRARY
# ============================================================

VIDEO_LIBRARY = {
    "Low": [
        {
            "title": "Ankle Alphabet",
            "embed_url": "https://www.youtube.com/embed/j6ts-qdDhBY",
            "watch_url": "https://www.youtube.com/watch?v=j6ts-qdDhBY",
            "description": "Gentle ankle mobility demonstration."
        },
        {
            "title": "Towel Curl Exercise",
            "embed_url": "https://www.youtube.com/embed/ch9xNz0WBR8",
            "watch_url": "https://www.youtube.com/watch?v=ch9xNz0WBR8",
            "description": "Seated foot strengthening demonstration."
        }
    ],

    "Medium": [
        {
            "title": "Towel Curl Exercise",
            "embed_url": "https://www.youtube.com/embed/ch9xNz0WBR8",
            "watch_url": "https://www.youtube.com/watch?v=ch9xNz0WBR8",
            "description": "Seated foot strengthening demonstration."
        },
        {
            "title": "Marble Pickup",
            "embed_url": "https://www.youtube.com/embed/TiYKMf6Rb8k",
            "watch_url": "https://www.youtube.com/watch?v=TiYKMf6Rb8k",
            "description": "Seated toe-control activity demonstration."
        }
    ],

    "High": [
        {
            "title": "Towel Curl Exercise",
            "embed_url": "https://www.youtube.com/embed/ch9xNz0WBR8",
            "watch_url": "https://www.youtube.com/watch?v=ch9xNz0WBR8",
            "description": "Seated foot strengthening demonstration."
        },
        {
            "title": "Ankle Alphabet",
            "embed_url": "https://www.youtube.com/embed/j6ts-qdDhBY",
            "watch_url": "https://www.youtube.com/watch?v=j6ts-qdDhBY",
            "description": "Gentle ankle mobility demonstration."
        },
        {
            "title": "Marble Pickup",
            "embed_url": "https://www.youtube.com/embed/TiYKMf6Rb8k",
            "watch_url": "https://www.youtube.com/watch?v=TiYKMf6Rb8k",
            "description": "Seated toe-control activity demonstration."
        }
    ]
}


# ============================================================
# CARE PLAN
# ============================================================

def get_care_plan(risk_level):

    plans = {
        "Low": {
            "title": "Low Risk Care Plan",
            "summary": (
                "The assessment shows a low-risk pattern based "
                "on the entered project features."
            ),
            "care_details": [
                "Keep daily activity comfortable and gradual.",
                "Use comfortable and supportive footwear.",
                "Take breaks during prolonged standing or walking.",
                "Avoid forcing painful movements.",
                "Monitor changes in symptoms.",
                "If symptoms persist or worsen, seek professional guidance."
            ],
            "daily_routine": [
                "Morning: begin with gentle comfortable movement.",
                "Daytime: use comfortable footwear.",
                "Take short breaks during prolonged standing.",
                "Evening: allow adequate recovery time.",
                "Monitor any persistent or worsening symptoms."
            ],
            "footwear": [
                "Choose comfortable and stable footwear.",
                "Avoid footwear that causes rubbing or pressure.",
                "Use footwear suitable for the activity.",
                "Replace footwear when it becomes excessively worn."
            ],
            "nutrition": [
                "Eat regular balanced meals.",
                "Include vegetables and fruits.",
                "Include protein-rich foods.",
                "Choose a variety of nutrient-rich foods.",
                "Drink water regularly."
            ]
        },

        "Medium": {
            "title": "Medium Risk Care Plan",
            "summary": (
                "The assessment shows a medium-risk pattern based "
                "on the entered project features."
            ),
            "care_details": [
                "Keep activity gradual and comfortable.",
                "Use supportive and comfortable footwear.",
                "Avoid long periods of continuous standing when possible.",
                "Take regular activity breaks.",
                "Avoid movements that increase discomfort.",
                "If symptoms persist or worsen, seek professional guidance."
            ],
            "daily_routine": [
                "Morning: start with gentle comfortable movement.",
                "During the day: take breaks from prolonged standing.",
                "Use comfortable footwear during walking.",
                "Avoid sudden increases in strenuous activity.",
                "Allow sufficient recovery time."
            ],
            "footwear": [
                "Choose footwear that feels comfortable and stable.",
                "Avoid footwear that creates pressure or rubbing.",
                "Use appropriate footwear for walking and daily activities.",
                "Check footwear condition regularly."
            ],
            "nutrition": [
                "Maintain regular balanced meals.",
                "Include vegetables, fruits and whole grains.",
                "Include varied protein foods.",
                "Stay hydrated throughout the day.",
                "Choose a variety of nutrient-rich foods."
            ]
        },

        "High": {
            "title": "High Risk Care Plan",
            "summary": (
                "The assessment shows a higher-risk pattern based "
                "on the entered project features."
            ),
            "care_details": [
                "Keep activity within a comfortable range.",
                "Avoid sudden increases in strenuous activity.",
                "Use comfortable and supportive footwear.",
                "Take regular breaks from prolonged standing or walking.",
                "Do not force movements that cause discomfort.",
                "If symptoms persist or worsen, seek professional guidance."
            ],
            "daily_routine": [
                "Morning: begin slowly with comfortable movement.",
                "During the day: reduce prolonged continuous standing where possible.",
                "Take regular rest breaks.",
                "Avoid sudden increases in physical activity.",
                "Monitor persistent or worsening symptoms."
            ],
            "footwear": [
                "Choose comfortable, stable footwear.",
                "Avoid footwear that causes pressure or rubbing.",
                "Use activity-appropriate footwear.",
                "Replace excessively worn footwear."
            ],
            "nutrition": [
                "Maintain balanced and regular meals.",
                "Include vegetables and fruits.",
                "Include varied protein foods.",
                "Choose whole and nutrient-rich foods.",
                "Drink water regularly."
            ]
        }
    }

    selected_plan = dict(plans.get(risk_level, plans["Low"]))

    selected_plan["exercise_note"] = (
        "Use gentle and controlled demonstrations within a "
        "comfortable range. Stop if pain or discomfort develops."
    )

    return selected_plan


# ============================================================
# BMI CATEGORY
# ============================================================

def get_bmi_category(bmi_value):

    if bmi_value < 18.5:
        return "Underweight"

    elif bmi_value < 25:
        return "Healthy Range"

    elif bmi_value < 30:
        return "Overweight"

    return "Higher BMI Range"


# ============================================================
# RISK CALCULATION
# ============================================================

def calculate_risk(patient_data, prediction):

    score = 0

    yes_fields = [
        "plantar_pain",
        "morning_pain",
        "previous_injury",
        "heel_symptom",
        "arch_symptom",
        "swelling",
        "diabetes"
    ]

    for field in yes_fields:
        if patient_data.get(field) == "Yes":
            score += 1

    if patient_data.get("plantar_pain") == "Yes":
        score += 2

    if patient_data.get("morning_pain") == "Yes":
        score += 2

    try:
        standing_hours = float(
            patient_data.get("standing_hours", 0)
        )
    except (TypeError, ValueError):
        standing_hours = 0

    if standing_hours >= 8:
        score += 2
    elif standing_hours >= 5:
        score += 1

    if patient_data.get("walking_activity") == "No":
        score += 1

    if prediction == "Yes":
        score += 2

    if score >= 8:
        return "High"
    elif score >= 4:
        return "Medium"

    return "Low"


# ============================================================
# SHARED RESULT CONTEXT
# ============================================================

def get_saved_result():

    result = session.get("result")

    if not isinstance(result, dict):
        return None

    return result


def normalize_risk_level(value):

    value = str(value or "Low").strip().title()

    if value not in ("Low", "Medium", "High"):
        return "Low"

    return value


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index")
def index():
    return redirect(url_for("home"))


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        ).strip()

        if not username:
            flash("Please enter your name.", "error")
            return redirect(url_for("login"))

        session["username"] = username

        return redirect(url_for("home"))

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ============================================================
# FEATURES
# ============================================================

@app.route("/features")
def features():
    return render_template("features.html")


# ============================================================
# PREDICTION PAGE
# ============================================================

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")


# ============================================================
# NORMALIZE YES/NO INPUTS
# ============================================================

def normalize_answer(value):

    value = str(value or "No").strip().title()

    if value not in ("Yes", "No"):
        return "No"

    return value


# ============================================================
# PREDICTION PROCESSING
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    name = request.form.get("name", "").strip()

    age = request.form.get("age", "").strip()
    height = request.form.get("height", "").strip()
    weight = request.form.get("weight", "").strip()

    standing_hours = request.form.get(
        "standing_hours", "0"
    ).strip()

    plantar_pain = normalize_answer(
        request.form.get("plantar_pain", "No")
    )

    morning_pain = normalize_answer(
        request.form.get("morning_pain", "No")
    )

    walking_activity = normalize_answer(
        request.form.get("walking_activity", "No")
    )

    previous_injury = normalize_answer(
        request.form.get("previous_injury", "No")
    )

    heel_symptom = normalize_answer(
        request.form.get("heel_symptom", "No")
    )

    arch_symptom = normalize_answer(
        request.form.get("arch_symptom", "No")
    )

    swelling = normalize_answer(
        request.form.get("swelling", "No")
    )

    diabetes = normalize_answer(
        request.form.get("diabetes", "No")
    )

    # Validate numeric inputs
    try:
        age_value = int(age)
        height_value = float(height)
        weight_value = float(weight)
        standing_value = float(standing_hours)

    except (TypeError, ValueError):
        flash(
            "Please enter valid numeric values for age, height, weight and standing hours.",
            "error"
        )
        return redirect(url_for("prediction"))

    # Validate input ranges
    if not (1 <= age_value <= 120):
        flash("Please enter a valid age.", "error")
        return redirect(url_for("prediction"))

    if not (30 <= height_value <= 250):
        flash("Please enter a valid height in centimetres.", "error")
        return redirect(url_for("prediction"))

    if not (2 <= weight_value <= 400):
        flash("Please enter a valid weight in kilograms.", "error")
        return redirect(url_for("prediction"))

    if not (0 <= standing_value <= 24):
        flash(
            "Standing hours must be between 0 and 24.",
            "error"
        )
        return redirect(url_for("prediction"))

    # Patient data
    patient_data = {
        "name": name or session.get("username", "User"),
        "age": age_value,
        "height": height_value,
        "weight": weight_value,
        "standing_hours": standing_value,
        "plantar_pain": plantar_pain,
        "morning_pain": morning_pain,
        "walking_activity": walking_activity,
        "previous_injury": previous_injury,
        "heel_symptom": heel_symptom,
        "arch_symptom": arch_symptom,
        "swelling": swelling,
        "diabetes": diabetes
    }

    # Machine learning input
    model_input = pd.DataFrame(
        [[
            age_value,
            height_value,
            weight_value,
            plantar_pain,
            morning_pain,
            standing_value,
            walking_activity,
            previous_injury,
            heel_symptom,
            arch_symptom,
            swelling,
            diabetes
        ]],
        columns=[
            "Age",
            "HeightCm",
            "WeightKg",
            "PlantarPain",
            "MorningPain",
            "StandingHours",
            "WalkingActivity",
            "PreviousInjury",
            "HeelSymptom",
            "ArchSymptom",
            "Swelling",
            "Diabetes"
        ]
    )

    # Machine learning prediction
    prediction_value = "Not Available"
    confidence = 0

    if model is not None:

        try:
            model_prediction = model.predict(model_input)[0]

            if str(model_prediction).strip().lower() in (
                "yes", "1", "true"
            ):
                prediction_value = "Yes"
            else:
                prediction_value = "No"

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(
                    model_input
                )[0]

                confidence = round(
                    float(max(probabilities)) * 100,
                    1
                )

        except Exception as error:
            print("Prediction error:", error)
            prediction_value = "Not Available"
            confidence = 0

    # BMI calculation
    height_meters = height_value / 100

    bmi = round(
        weight_value / (height_meters ** 2),
        2
    )

    bmi_category = get_bmi_category(bmi)

    # Risk level
    risk_level = calculate_risk(
        patient_data,
        prediction_value
    )

    # Feature summary
    feature_summary = {
        "Age": age_value,
        "Height": f"{height_value:.1f} cm",
        "Weight": f"{weight_value:.1f} kg",
        "BMI": bmi,
        "BMI Category": bmi_category,
        "Plantar Pain": plantar_pain,
        "Morning Pain": morning_pain,
        "Standing Hours": standing_value,
        "Walking Activity": walking_activity,
        "Previous Injury": previous_injury,
        "Heel Symptom": heel_symptom,
        "Arch Symptom": arch_symptom,
        "Swelling": swelling,
        "Diabetes": diabetes
    }

    # Store all results in one dictionary
    result = {
        "patient": {
            "name": patient_data["name"],
            "age": age_value,
            "height": height_value,
            "weight": weight_value
        },
        "bmi": bmi,
        "bmi_category": bmi_category,
        "prediction": prediction_value,
        "risk_level": risk_level,
        "confidence": confidence,
        "feature_summary": feature_summary,
        "generated_at": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )
    }

    # Save results in session
    session["result"] = result
    session["risk_level"] = risk_level

    return redirect(url_for("prediction_result"))


# ============================================================
# PREDICTION RESULT PAGE
# ============================================================

@app.route("/prediction-result")
def prediction_result():

    result = get_saved_result()

    if not result:
        flash(
            "Please complete the prediction assessment first.",
            "error"
        )
        return redirect(url_for("prediction"))

    patient = result.get("patient", {})

    if not isinstance(patient, dict):
        patient = {}

    risk_level = normalize_risk_level(
        result.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    videos = VIDEO_LIBRARY.get(
        risk_level,
        VIDEO_LIBRARY["Low"]
    )

    return render_template(
        "prediction-result.html",
        result=result,
        patient=patient,
        bmi=result.get("bmi", "N/A"),
        bmi_category=result.get("bmi_category", "N/A"),
        prediction=result.get("prediction", "Not Available"),
        confidence=result.get("confidence", 0),
        generated_at=result.get("generated_at", "N/A"),
        risk_level=risk_level,
        risk_info=risk_info,
        videos=videos
    )


# ============================================================
# GENERAL CARE
# ============================================================

@app.route("/care")
def care():

    result = get_saved_result()

    risk_level = normalize_risk_level(
        session.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    return render_template(
        "plantar-care.html",
        result=result,
        risk_level=risk_level,
        risk_info=risk_info
    )


# ============================================================
# DAILY ROUTINE
# ============================================================

@app.route("/daily-routine")
def daily_routine():

    result = get_saved_result()

    risk_level = normalize_risk_level(
        session.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    return render_template(
        "daily-routine.html",
        result=result,
        risk_level=risk_level,
        risk_info=risk_info
    )


# ============================================================
# FOOTWEAR
# ============================================================

@app.route("/footwear")
def footwear():

    result = get_saved_result()

    risk_level = normalize_risk_level(
        session.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    return render_template(
        "footwear.html",
        result=result,
        risk_level=risk_level,
        risk_info=risk_info
    )


# ============================================================
# NUTRITION
# ============================================================

@app.route("/nutrition")
def nutrition():

    result = get_saved_result()

    risk_level = normalize_risk_level(
        session.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    return render_template(
        "nutrition.html",
        result=result,
        risk_level=risk_level,
        risk_info=risk_info
    )


# ============================================================
# EXERCISE
# ============================================================

@app.route("/exercise")
def exercise():

    result = get_saved_result()

    risk_level = normalize_risk_level(
        session.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    videos = VIDEO_LIBRARY.get(
        risk_level,
        VIDEO_LIBRARY["Low"]
    )

    return render_template(
        "exercise.html",
        result=result,
        risk_level=risk_level,
        risk_info=risk_info,
        videos=videos
    )


# ============================================================
# CAMERA GAMES
# ============================================================

@app.route("/games")
def games():

    result = get_saved_result()

    risk_level = normalize_risk_level(
        session.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    return render_template(
        "games.html",
        result=result,
        risk_level=risk_level,
        risk_info=risk_info
    )


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():
    return render_template("about.html")


# ============================================================
# REPORT PAGE - FIXED
# ============================================================

@app.route("/report")
def report():

    result = get_saved_result()

    if not result:
        flash(
            "Please complete the prediction assessment first.",
            "error"
        )
        return redirect(url_for("prediction"))

    # FIX: retrieve patient from the saved result
    patient = result.get("patient", {})

    if not isinstance(patient, dict):
        patient = {}

    risk_level = normalize_risk_level(
        result.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    # FIX: pass every variable required by report.html
    return render_template(
        "report.html",
        result=result,
        patient=patient,
        bmi=result.get("bmi", "N/A"),
        bmi_category=result.get("bmi_category", "N/A"),
        prediction=result.get("prediction", "Not Available"),
        confidence=result.get("confidence", 0),
        generated_at=result.get("generated_at", "N/A"),
        risk_level=risk_level,
        risk_info=risk_info
    )


# ============================================================
# DOWNLOAD PDF REPORT
# ============================================================

@app.route("/download-report")
def download_report():

    result = get_saved_result()

    if not result:
        flash(
            "Please complete the prediction assessment first.",
            "error"
        )
        return redirect(url_for("prediction"))

    risk_level = normalize_risk_level(
        result.get("risk_level", "Low")
    )

    risk_info = get_care_plan(risk_level)

    # Patient information
    patient = result.get("patient", {})

    if not isinstance(patient, dict):
        patient = {}

    patient_name = str(
        patient.get("name") or "User"
    ).strip()

    safe_name = "".join(
        char if char.isalnum() or char in ("-", "_") else "_"
        for char in patient_name
    ).strip("_")

    if not safe_name:
        safe_name = "User"

    report_filename = f"PLANTARCARE_Report_{safe_name}.pdf"

    report_path = os.path.join(
        REPORT_FOLDER,
        report_filename
    )

    # PDF document
    document = SimpleDocTemplate(
        report_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    story = []

    # Title
    story.append(
        Paragraph("PLANTARCARE", title_style)
    )

    story.append(
        Paragraph(
            "Plantar Fasciitis Risk Prediction System",
            heading_style
        )
    )

    story.append(Spacer(1, 15))

    # Report information
    story.append(
        Paragraph("Assessment Report", heading_style)
    )

    generated_at = escape(
        str(result.get("generated_at", ""))
    )

    story.append(
        Paragraph(
            f"Generated Date and Time: {generated_at}",
            normal_style
        )
    )

    story.append(Spacer(1, 12))

    # Patient information
    story.append(
        Paragraph("Patient Information", heading_style)
    )

    patient_table_data = [
        ["Name", str(patient.get("name", "User"))],
        ["Age", str(patient.get("age", ""))],
        ["Height", f'{patient.get("height", "")} cm'],
        ["Weight", f'{patient.get("weight", "")} kg'],
        ["BMI", str(result.get("bmi", ""))],
        ["BMI Category", str(result.get("bmi_category", ""))]
    ]

    patient_table = Table(
        patient_table_data,
        colWidths=[150, 300]
    )

    patient_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(patient_table)
    story.append(Spacer(1, 15))

    # Prediction result
    story.append(
        Paragraph("Prediction Result", heading_style)
    )

    confidence_value = result.get("confidence", 0)
    confidence_text = str(confidence_value).strip()

    if confidence_text.endswith("%"):
        confidence_text = confidence_text[:-1].strip()

    prediction_table_data = [
        [
            "Machine Learning Prediction",
            str(result.get("prediction", "Not Available"))
        ],
        [
            "Confidence",
            f"{confidence_text}%"
        ],
        [
            "Risk Level",
            risk_level
        ]
    ]

    prediction_table = Table(
        prediction_table_data,
        colWidths=[250, 200]
    )

    prediction_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(prediction_table)
    story.append(Spacer(1, 15))

    # Assessment features
    story.append(
        Paragraph("Assessment Features", heading_style)
    )

    feature_rows = [["Feature", "Value"]]

    feature_summary = result.get("feature_summary", {})

    if not isinstance(feature_summary, dict):
        feature_summary = {}

    for feature, value in feature_summary.items():
        feature_rows.append([
            str(feature),
            str(value)
        ])

    feature_table = Table(
        feature_rows,
        colWidths=[250, 200],
        repeatRows=1
    )

    feature_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )

    story.append(feature_table)
    story.append(Spacer(1, 15))

    # Care guidance
    story.append(
        Paragraph("General Care Guidance", heading_style)
    )

    story.append(
        Paragraph(
            escape(str(risk_info.get("summary", ""))),
            normal_style
        )
    )

    story.append(Spacer(1, 8))

    for item in risk_info.get("care_details", []):
        story.append(
            Paragraph(
                "&#8226; " + escape(str(item)),
                normal_style
            )
        )
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # Daily routine
    story.append(
        Paragraph("Daily Routine", heading_style)
    )

    for item in risk_info.get("daily_routine", []):
        story.append(
            Paragraph(
                "&#8226; " + escape(str(item)),
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    # Footwear guidance
    story.append(
        Paragraph("Footwear Guidance", heading_style)
    )

    for item in risk_info.get("footwear", []):
        story.append(
            Paragraph(
                "&#8226; " + escape(str(item)),
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    # Nutrition guidance
    story.append(
        Paragraph("Nutrition Guidance", heading_style)
    )

    for item in risk_info.get("nutrition", []):
        story.append(
            Paragraph(
                "&#8226; " + escape(str(item)),
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    # Exercise guidance
    story.append(
        Paragraph("Exercise Guidance", heading_style)
    )

    story.append(
        Paragraph(
            escape(str(risk_info.get("exercise_note", ""))),
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Disclaimer
    story.append(
        Paragraph(
            "<b>Disclaimer:</b> PLANTARCARE is an academic "
            "machine learning project designed for educational "
            "and awareness purposes. The prediction should not "
            "be considered a medical diagnosis. Users should "
            "consult a qualified healthcare professional for "
            "medical evaluation and treatment.",
            normal_style
        )
    )

    # Build PDF
    try:
        document.build(story)

    except Exception as error:
        print("PDF generation error:", error)
        flash(
            "Unable to generate the PDF report. Please try again.",
            "error"
        )
        return redirect(url_for("report"))

    return send_file(
        report_path,
        as_attachment=True,
        download_name=report_filename
    )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
