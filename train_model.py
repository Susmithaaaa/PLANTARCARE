import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "plantar_risk_prediction_dataset.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "plantarcare_model.pkl"
)


# ============================================================
# FEATURES
# ============================================================

FEATURE_COLUMNS = [

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


TARGET = "PlantarFasciitis"


# ============================================================
# NUMERIC / CATEGORICAL COLUMNS
# ============================================================

NUMERIC_COLUMNS = [

    "Age",
    "HeightCm",
    "WeightKg",
    "StandingHours"
]


CATEGORICAL_COLUMNS = [

    column
    for column in FEATURE_COLUMNS
    if column not in NUMERIC_COLUMNS
]


YES_NO_COLUMNS = (
    CATEGORICAL_COLUMNS
    + [TARGET]
)


# ============================================================
# LOAD DATASET
# ============================================================

print(
    "\nLoading dataset..."
)

df = pd.read_csv(
    DATA_FILE
)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = (
    FEATURE_COLUMNS
    + [TARGET]
)

missing_columns = [

    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    raise ValueError(

        "Missing columns in dataset: "
        + ", ".join(
            missing_columns
        )
    )


# ============================================================
# KEEP REQUIRED COLUMNS
# ============================================================

df = df[
    required_columns
].copy()


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

for column in NUMERIC_COLUMNS:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# NORMALIZE YES / NO VALUES
# ============================================================

for column in YES_NO_COLUMNS:

    df[column] = (

        df[column]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({

            "yes": "Yes",
            "no": "No",

            "1": "Yes",
            "0": "No",

            "true": "Yes",
            "false": "No"
        })
    )


# ============================================================
# REMOVE INVALID TARGET ROWS
# ============================================================

df = df.dropna(
    subset=[TARGET]
)


# ============================================================
# INPUT / TARGET
# ============================================================

X = df[
    FEATURE_COLUMNS
]

y = df[
    TARGET
]


print(
    "\nDataset rows:",
    len(df)
)

print(
    "Features:",
    len(FEATURE_COLUMNS)
)

print(
    "Target:",
    TARGET
)


# ============================================================
# PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline([

    (
        "imputer",
        SimpleImputer(
            strategy="median"
        )
    )
])


categorical_pipeline = Pipeline([

    (
        "imputer",
        SimpleImputer(
            strategy="most_frequent"
        )
    ),

    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])


preprocessor = ColumnTransformer([

    (
        "numeric",
        numeric_pipeline,
        NUMERIC_COLUMNS
    ),

    (
        "categorical",
        categorical_pipeline,
        CATEGORICAL_COLUMNS
    )
])


# ============================================================
# RANDOM FOREST MODEL
# ============================================================

random_forest = RandomForestClassifier(

    n_estimators=200,

    random_state=42,

    class_weight="balanced",

    min_samples_leaf=1,

    n_jobs=-1
)


# ============================================================
# COMPLETE PIPELINE
# ============================================================

pipeline = Pipeline([

    (
        "preprocessor",
        preprocessor
    ),

    (
        "random_forest",
        random_forest
    )
])


# ============================================================
# VALIDATION
# ============================================================

if (
    len(df) >= 10
    and y.nunique() > 1
):

    try:

        class_counts = (
            y.value_counts()
        )

        can_stratify = (
            class_counts.min() >= 2
        )

        if can_stratify:

            X_train, X_test, y_train, y_test = train_test_split(

                X,
                y,

                test_size=0.2,

                random_state=42,

                stratify=y
            )

        else:

            X_train, X_test, y_train, y_test = train_test_split(

                X,
                y,

                test_size=0.2,

                random_state=42
            )


        pipeline.fit(
            X_train,
            y_train
        )


        predictions = pipeline.predict(
            X_test
        )


        accuracy = accuracy_score(
            y_test,
            predictions
        )


        print(
            "\nValidation Accuracy:",
            round(
                accuracy * 100,
                2
            ),
            "%"
        )

    except Exception as error:

        print(
            "\nValidation skipped:",
            error
        )


# ============================================================
# TRAIN FINAL MODEL USING COMPLETE DATASET
# ============================================================

print(
    "\nTraining final model..."
)

pipeline.fit(
    X,
    y
)


# ============================================================
# SAVE MODEL PACKAGE
# ============================================================

model_package = {

    "model":
        pipeline,

    "features":
        FEATURE_COLUMNS,

    "target":
        TARGET,

    "numeric_features":
        NUMERIC_COLUMNS,

    "categorical_features":
        CATEGORICAL_COLUMNS
}


joblib.dump(
    model_package,
    MODEL_FILE
)


print(
    "\nModel saved successfully:"
)

print(
    MODEL_FILE
)

print(
    "\nPLANTARCARE model training completed."
)