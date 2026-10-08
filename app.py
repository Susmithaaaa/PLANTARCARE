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

app.secret_key = "plantarcare-secret-key-2026"


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "plantarcare_model.pkl"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

model = None

try:

    package = joblib.load(
        MODEL_FILE
    )

    if isinstance(package, dict):

        model = package.get(
            "model"
        )

    else:

        model = package

    print(
        "PLANTARCARE model loaded successfully."
    )

except Exception as error:

    print(
        "Model loading error:",
        error
    )

    model = None


# ============================================================
# VIDEO LIBRARY
# ============================================================

VIDEO_LIBRARY = {

    "Low": [

        {
            "title": "Ankle Alphabet",

            "embed_url":
                "https://www.youtube.com/embed/j6ts-qdDhBY",

            "watch_url":
                "https://www.youtube.com/watch?v=j6ts-qdDhBY",

            "description":
                "Gentle ankle mobility demonstration."
        },

        {
            "title": "Towel Curl Exercise",

            "embed_url":
                "https://www.youtube.com/embed/ch9xNz0WBR8",

            "watch_url":
                "https://www.youtube.com/watch?v=ch9xNz0WBR8",

            "description":
                "Seated foot strengthening demonstration."
        }

    ],


    "Medium": [

        {
            "title": "Towel Curl Exercise",

            "embed_url":
                "https://www.youtube.com/embed/ch9xNz0WBR8",

            "watch_url":
                "https://www.youtube.com/watch?v=ch9xNz0WBR8",

            "description":
                "Seated foot strengthening demonstration."
        },

        {
            "title": "Marble Pickup",

            "embed_url":
                "https://www.youtube.com/embed/TiYKMf6Rb8k",

            "watch_url":
                "https://www.youtube.com/watch?v=TiYKMf6Rb8k",

            "description":
                "Seated toe-control activity demonstration."
        }

    ],


    "High": [

        {
            "title": "Towel Curl Exercise",

            "embed_url":
                "https://www.youtube.com/embed/ch9xNz0WBR8",

            "watch_url":
                "https://www.youtube.com/watch?v=ch9xNz0WBR8",

            "description":
                "Seated foot strengthening demonstration."
        },

        {
            "title": "Ankle Alphabet",

            "embed_url":
                "https://www.youtube.com/embed/j6ts-qdDhBY",

            "watch_url":
                "https://www.youtube.com/watch?v=j6ts-qdDhBY",

            "description":
                "Gentle ankle mobility demonstration."
        },

        {
            "title": "Marble Pickup",

            "embed_url":
                "https://www.youtube.com/embed/TiYKMf6Rb8k",

            "watch_url":
                "https://www.youtube.com/watch?v=TiYKMf6Rb8k",

            "description":
                "Seated toe-control activity demonstration."
        }

    ]

}


# ============================================================
# CARE PLAN
# ============================================================

def get_care_plan(risk_level):

    plans = {

        "Low": {

            "title":
                "Low Risk Care Plan",

            "summary":
                "The assessment shows a low-risk pattern based on the entered project features.",

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

            "title":
                "Medium Risk Care Plan",

            "summary":
                "The assessment shows a medium-risk pattern based on the entered project features.",

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

            "title":
                "High Risk Care Plan",

            "summary":
                "The assessment shows a higher-risk pattern based on the entered project features.",

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


    selected_plan = plans.get(
        risk_level,
        plans["Low"]
    )


    selected_plan["exercise_note"] = (
        "Use gentle and controlled demonstrations "
        "within a comfortable range. "
        "Stop if pain or discomfort develops."
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

    else:

        return "Higher BMI Range"


# ============================================================
# RISK CALCULATION
# ============================================================

def calculate_risk(
    patient_data,
    prediction
):

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


    if patient_data.get(
        "plantar_pain"
    ) == "Yes":

        score += 2


    if patient_data.get(
        "morning_pain"
    ) == "Yes":

        score += 2


    try:

        standing_hours = float(
            patient_data.get(
                "standing_hours",
                0
            )
        )

    except Exception:

        standing_hours = 0


    if standing_hours >= 8:

        score += 2

    elif standing_hours >= 5:

        score += 1


    if patient_data.get(
        "walking_activity"
    ) == "No":

        score += 1


    if prediction == "Yes":

        score += 2


    if score >= 8:

        return "High"

    elif score >= 4:

        return "Medium"

    else:

        return "Low"


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# INDEX
# ============================================================

@app.route("/index")
def index():

    return redirect(
        url_for("home")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        if username:

            session["username"] = username

            return redirect(
                url_for("home")
            )


        flash(
            "Please enter your username."
        )


    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# FEATURES
# ============================================================

@app.route("/features")
def features():

    return render_template(
        "features.html"
    )


# ============================================================
# PREDICTION PAGE
# IMPORTANT:
# THIS ROUTE MUST EXIST ONLY ONCE
# ============================================================

@app.route("/prediction")
def prediction():

    return render_template(
        "prediction.html"
    )


# ============================================================
# PREDICTION PROCESSING
# IMPORTANT:
# FORM MUST POST TO /predict
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    if model is None:

        flash(
            "Machine learning model not found. "
            "Please run train_model.py first."
        )

        return redirect(
            url_for("prediction")
        )


    try:

        form = request.form


        name = form.get(
            "name",
            "User"
        )


        age = float(
            form["age"]
        )


        height = float(
            form["height"]
        )


        weight = float(
            form["weight"]
        )


        standing_hours = float(
            form["standing_hours"]
        )


        plantar_pain = form[
            "plantar_pain"
        ]


        morning_pain = form[
            "morning_pain"
        ]


        walking_activity = form[
            "walking_activity"
        ]


        previous_injury = form[
            "previous_injury"
        ]


        heel_symptom = form[
            "heel_symptom"
        ]


        arch_symptom = form[
            "arch_symptom"
        ]


        swelling = form[
            "swelling"
        ]


        diabetes = form[
            "diabetes"
        ]


        # ----------------------------------------------------
        # PATIENT DATA
        # ----------------------------------------------------

        patient_data = {

            "name": name,

            "age": age,

            "height": height,

            "weight": weight,

            "standing_hours":
                standing_hours,

            "plantar_pain":
                plantar_pain,

            "morning_pain":
                morning_pain,

            "walking_activity":
                walking_activity,

            "previous_injury":
                previous_injury,

            "heel_symptom":
                heel_symptom,

            "arch_symptom":
                arch_symptom,

            "swelling":
                swelling,

            "diabetes":
                diabetes

        }


        # ----------------------------------------------------
        # MODEL INPUT
        # ----------------------------------------------------

        model_input = pd.DataFrame([{

            "Age": age,

            "HeightCm": height,

            "WeightKg": weight,

            "PlantarPain":
                plantar_pain,

            "MorningPain":
                morning_pain,

            "StandingHours":
                standing_hours,

            "WalkingActivity":
                walking_activity,

            "PreviousInjury":
                previous_injury,

            "HeelSymptom":
                heel_symptom,

            "ArchSymptom":
                arch_symptom,

            "Swelling":
                swelling,

            "Diabetes":
                diabetes

        }])


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        model_prediction = model.predict(
            model_input
        )[0]


        prediction_text = (

            "Yes"

            if str(
                model_prediction
            ).lower()
            in [
                "yes",
                "1",
                "true"
            ]

            else "No"

        )


        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        confidence = "N/A"


        if hasattr(
            model,
            "predict_proba"
        ):

            probability = model.predict_proba(
                model_input
            )[0]


            confidence = round(
                float(
                    max(probability)
                ) * 100,
                1
            )


        # ----------------------------------------------------
        # BMI
        # ----------------------------------------------------

        bmi = weight / (
            (height / 100) ** 2
        )


        bmi = round(
            bmi,
            1
        )


        bmi_category = get_bmi_category(
            bmi
        )


        # ----------------------------------------------------
        # RISK
        # ----------------------------------------------------

        risk_level = calculate_risk(
            patient_data,
            prediction_text
        )


        # ----------------------------------------------------
        # FEATURE SUMMARY
        # ----------------------------------------------------

        feature_summary = {

            "Plantar Pain":
                plantar_pain,

            "Morning Pain":
                morning_pain,

            "Walking Activity":
                walking_activity,

            "Previous Injury":
                previous_injury,

            "Heel Symptoms":
                heel_symptom,

            "Arch Symptoms":
                arch_symptom,

            "Swelling":
                swelling,

            "Diabetes":
                diabetes

        }


        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        result = {

            "patient":
                patient_data,

            "bmi":
                bmi,

            "bmi_category":
                bmi_category,

            "prediction":
                prediction_text,

            "risk_level":
                risk_level,

            "confidence":
                confidence,

            "feature_summary":
                feature_summary,

            "generated_at":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )

        }


        # ----------------------------------------------------
        # SESSION
        # ----------------------------------------------------

        session["result"] = result

        session["risk_level"] = risk_level


        # ----------------------------------------------------
        # RESULT PAGE
        # ----------------------------------------------------

        return redirect(
            url_for(
                "prediction_result"
            )
        )


    except Exception as error:

        print(
            "Prediction error:",
            error
        )


        flash(
            "Please check all entered values "
            "and Yes/No selections."
        )


        return redirect(
            url_for("prediction")
        )


# ============================================================
# PREDICTION RESULT
# ============================================================

@app.route("/prediction-result")
def prediction_result():

    result = session.get(
        "result"
    )


    if not result:

        return redirect(
            url_for("prediction")
        )


    risk_level = result.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    videos = VIDEO_LIBRARY.get(
        risk_level,
        VIDEO_LIBRARY["Low"]
    )


    return render_template(

        "prediction-result.html",

        patient=result.get(
            "patient",
            {}
        ),

        bmi=result.get(
            "bmi"
        ),

        bmi_category=result.get(
            "bmi_category"
        ),

        prediction=result.get(
            "prediction"
        ),

        risk_level=risk_level,

        confidence=result.get(
            "confidence"
        ),

        feature_summary=result.get(
            "feature_summary",
            {}
        ),

        generated_at=result.get(
            "generated_at"
        ),

        risk_info=risk_info,

        videos=videos

    )


# ============================================================
# CARE PAGE
# ============================================================

@app.route("/care")
def care():

    risk_level = session.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    return render_template(

        "plantar-care.html",

        risk_level=risk_level,

        risk_info=risk_info

    )


# ============================================================
# DAILY ROUTINE
# ============================================================

@app.route("/daily-routine")
def daily_routine():

    risk_level = session.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    return render_template(

        "daily-routine.html",

        risk_level=risk_level,

        risk_info=risk_info

    )


# ============================================================
# FOOTWEAR
# ============================================================

@app.route("/footwear")
def footwear():

    risk_level = session.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    return render_template(

        "footwear.html",

        risk_level=risk_level,

        risk_info=risk_info

    )


# ============================================================
# NUTRITION
# ============================================================

@app.route("/nutrition")
def nutrition():

    risk_level = session.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    return render_template(

        "nutrition.html",

        risk_level=risk_level,

        risk_info=risk_info

    )


# ============================================================
# EXERCISE
# ============================================================

@app.route("/exercise")
def exercise():

    risk_level = session.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    videos = VIDEO_LIBRARY.get(
        risk_level,
        VIDEO_LIBRARY["Low"]
    )


    return render_template(

        "exercise.html",

        risk_level=risk_level,

        risk_info=risk_info,

        videos=videos

    )


# ============================================================
# GAMES
# ============================================================

@app.route("/games")
def games():

    return render_template(
        "games.html"
    )


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ============================================================
# REPORT PAGE
# ============================================================

@app.route("/report")
def report():

    result = session.get(
        "result"
    )


    if not result:

        return redirect(
            url_for("prediction")
        )


    risk_level = result.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    return render_template(

        "report.html",

        patient=result.get(
            "patient",
            {}
        ),

        bmi=result.get(
            "bmi"
        ),

        bmi_category=result.get(
            "bmi_category"
        ),

        prediction=result.get(
            "prediction"
        ),

        risk_level=risk_level,

        confidence=result.get(
            "confidence"
        ),

        feature_summary=result.get(
            "feature_summary",
            {}
        ),

        generated_at=result.get(
            "generated_at"
        ),

        risk_info=risk_info

    )


# ============================================================
# DOWNLOAD PDF REPORT
# ============================================================

@app.route("/download-report")
def download_report():

    result = session.get(
        "result"
    )


    if not result:

        return redirect(
            url_for("prediction")
        )


    patient = result.get(
        "patient",
        {}
    )


    risk_level = result.get(
        "risk_level",
        "Low"
    )


    risk_info = get_care_plan(
        risk_level
    )


    file_name = (
        "PLANTARCARE_Report_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".pdf"
    )


    file_path = os.path.join(
        REPORT_FOLDER,
        file_name
    )


    try:

        document = SimpleDocTemplate(

            file_path,

            pagesize=A4,

            rightMargin=40,

            leftMargin=40,

            topMargin=40,

            bottomMargin=40

        )


        styles = getSampleStyleSheet()


        story = []


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        story.append(

            Paragraph(
                "PLANTARCARE",
                styles["Title"]
            )

        )


        story.append(

            Paragraph(
                "PLANTAR FASCIITIS RISK "
                "PREDICTION REPORT",
                styles["Heading2"]
            )

        )


        story.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # PATIENT DETAILS
        # ----------------------------------------------------

        story.append(

            Paragraph(
                "Patient Information",
                styles["Heading2"]
            )

        )


        patient_table = Table([

            [
                "Name",
                str(
                    patient.get(
                        "name",
                        "User"
                    )
                )
            ],

            [
                "Age",
                str(
                    patient.get(
                        "age",
                        "-"
                    )
                )
            ],

            [
                "Height",
                str(
                    patient.get(
                        "height",
                        "-"
                    )
                ) + " cm"
            ],

            [
                "Weight",
                str(
                    patient.get(
                        "weight",
                        "-"
                    )
                ) + " kg"
            ],

            [
                "BMI",
                str(
                    result.get(
                        "bmi",
                        "-"
                    )
                )
            ],

            [
                "BMI Category",
                str(
                    result.get(
                        "bmi_category",
                        "-"
                    )
                )
            ]

        ])


        patient_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])

        )


        story.append(
            patient_table
        )


        story.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        story.append(

            Paragraph(
                "Prediction Result",
                styles["Heading2"]
            )

        )


        prediction_table = Table([

            [
                "Risk Level",
                str(
                    result.get(
                        "risk_level",
                        "-"
                    )
                )
            ],

            [
                "ML Prediction",
                str(
                    result.get(
                        "prediction",
                        "-"
                    )
                )
            ],

            [
                "Confidence",
                str(
                    result.get(
                        "confidence",
                        "-"
                    )
                )
            ],

            [
                "Generated",
                str(
                    result.get(
                        "generated_at",
                        "-"
                    )
                )
            ]

        ])


        prediction_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])

        )


        story.append(
            prediction_table
        )


        story.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # FEATURE SUMMARY
        # ----------------------------------------------------

        story.append(

            Paragraph(
                "Assessment Features",
                styles["Heading2"]
            )

        )


        feature_rows = [
            ["Feature", "Response"]
        ]


        for key, value in result.get(
            "feature_summary",
            {}
        ).items():

            feature_rows.append([

                str(key),

                str(value)

            ])


        feature_table = Table(
            feature_rows
        )


        feature_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])

        )


        story.append(
            feature_table
        )


        story.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # CARE GUIDANCE
        # ----------------------------------------------------

        story.append(

            Paragraph(
                "Care Guidance",
                styles["Heading2"]
            )

        )


        for item in risk_info.get(
            "care_details",
            []
        ):

            story.append(

                Paragraph(
                    "• " + item,
                    styles["BodyText"]
                )

            )

            story.append(
                Spacer(1, 5)
            )


        story.append(
            Spacer(1, 10)
        )


        # ----------------------------------------------------
        # DISCLAIMER
        # ----------------------------------------------------

        story.append(

            Paragraph(
                "PLANTARCARE is an academic project "
                "for preliminary risk awareness and "
                "educational support. The prediction "
                "is not a confirmed medical diagnosis. "
                "Persistent or concerning symptoms "
                "should be discussed with a qualified "
                "healthcare professional.",
                styles["BodyText"]
            )

        )


        # ----------------------------------------------------
        # BUILD PDF
        # ----------------------------------------------------

        document.build(
            story
        )


        return send_file(

            file_path,

            as_attachment=True,

            download_name=file_name

        )


    except Exception as error:

        print(
            "PDF generation error:",
            error
        )


        flash(
            "Unable to generate the PDF report."
        )


        return redirect(
            url_for("report")
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )