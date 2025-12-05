# Importing Important library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
import pickle

# load the dataset
smote_df = pd.read_csv("framingham.csv")

# some basic checking
print(smote_df.shape)
print(smote_df.head())

# drop unnecessary column and rename some columns
smote_df = smote_df.drop(columns=["education"], axis=1)
smote_df = smote_df.rename(columns={"male": "gender", "TenYearCHD": "CHD"})

# check the final dataset
print(smote_df.sample(20))

# splitting dataset into X & Y.
X = smote_df.drop("CHD", axis=1)
y = smote_df["CHD"]

# seprate X and Y into X_train, X_test, y_train, y_test by using train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# classification of numerical and categorical columns
num_cols = [
    "age",
    "cigsPerDay",
    "totChol",
    "sysBP",
    "diaBP",
    "BMI",
    "heartRate",
    "glucose",
]
cat_cols = [
    "gender",
    "currentSmoker",
    "prevalentStroke",
    "prevalentHyp",
    "diabetes",
    "BPMeds",
]

# Building pipeline for Numerical and categorical column
num_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("yeojohnson", PowerTransformer(method="yeo-johnson")),
        ("scaler", MinMaxScaler()),
    ]
)

cat_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]
)

# merge the numerical and categorical pipeline using columnTransformer.
preprocessor = ColumnTransformer(
    transformers=[("num", num_pipeline, num_cols), ("cat", cat_pipeline, cat_cols)]
)

# using Logistic regression.
logreg_pipeline = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        ("smote", SMOTE(random_state=42)),
        ("model", LogisticRegression(max_iter=500, class_weight="balanced")),
    ]
)

# fit the modewl on X_train and y_train
model = logreg_pipeline.fit(X_train, y_train)

# Evaluate the model
def evaluate_model(model, name):
    
    print("="*65)
    print(f"📌 Evaluating: {name}")
    print("="*65)

    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Basic metrics
    print(f"✔ Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\n📄 Classification Report:\n")
    print(classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("🔢 Confusion Matrix:\n", cm)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",xticklabels=["No CHD", "CHD"],yticklabels=["No CHD", "CHD"])
    plt.title(f"Confusion Matrix - {name}")
    plt.show()

    # =============================
    # 🚀 ROC Curve
    # =============================
    print(f"✔ ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
    
    fpr, tpr, thresholds = roc_curve(y_test, y_proba)

    plt.figure(figsize=(6,5))
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_test, y_proba):.4f}", linewidth=2)
    plt.plot([0,1], [0,1], "k--", label="Random Guess")
    
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve - {name}")
    plt.legend()
    plt.grid(True)
    plt.show()
    
evaluate_model(logreg_pipeline,"Logestic Regresssion")

# prediction in sample data.
sample_data = {
    "gender":1, "age":50, "currentSmoker":1, "cigsPerDay":35,
    "BPMeds":1, "prevalentStroke":1, "prevalentHyp":1, "diabetes":1,
    "totChol":420, "sysBP":179, "diaBP":92, "BMI":25.97,
    "heartRate":66, "glucose":112
}

sample_data = pd.DataFrame([sample_data])

lgpred = model.predict(sample_data)

print("Logisticprediction :", lgpred)

# Extract trained model
trained_model = model.named_steps["model"]
print(trained_model)

# Create clean pipeline for prediction because Smote is a training technique only not prediction.
deploy_pipeline = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        ("model", trained_model)
    ]
)

# Fit preprocess only (model weights remain same)
deploy_pipeline.fit(X_train, y_train)

# prediction on sample data using deploy_pipeline
sample_data = {
    "gender":1, "age":50, "currentSmoker":1, "cigsPerDay":35,
    "BPMeds":1, "prevalentStroke":1, "prevalentHyp":1, "diabetes":1,
    "totChol":420, "sysBP":179, "diaBP":92, "BMI":25.97,
    "heartRate":66, "glucose":112
}

sample_df = pd.DataFrame([sample_data])

prediction = deploy_pipeline.predict(sample_df)
print("Sample Prediction:", prediction)

# saved the modelin pickle file format
with open("heart_disease_model.pkl", "wb") as f:
    pickle.dump(deploy_pipeline, f)

print("🚀 Model saved successfully as 'heart_disease_model.pkl'")