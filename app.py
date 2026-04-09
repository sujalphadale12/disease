import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Set page config
st.set_page_config(page_title="Disease Prediction System", layout="wide")

# Helper to find the correct path for your local setup
def get_path(filename):
    # Check common locations for the models
    locations = [
        f'models/{filename}',
        f'disease_prediction/models/{filename}',
        filename
    ]
    for loc in locations:
        if os.path.exists(loc):
            return loc
    return None

@st.cache_resource
def load_resources():
    # Load the 3 models and the symptom list we trained
    rf_path = get_path('randomforest_model.pkl')
    svm_path = get_path('svm_model.pkl')
    nb_path = get_path('naivebayes_model.pkl')
    sym_path = get_path('symptoms_list.pkl')
    
    if not all([rf_path, svm_path, nb_path, sym_path]):
        return None, None, None, None

    rf_model = joblib.load(rf_path)
    svm_model = joblib.load(svm_path)
    nb_model = joblib.load(nb_path)
    symptoms_list = joblib.load(sym_path)
    return rf_model, svm_model, nb_model, symptoms_list

# UI Header
st.title("🩺 Disease Prediction System")
st.markdown("Predict potential diseases based on symptoms using Machine Learning.")

rf_model, svm_model, nb_model, symptoms_list = load_resources()

if rf_model is None:
    st.error("❌ Model files not found!")
    st.info("Please run 'python train_models.py' first to generate the model files in the 'models' folder.")
else:
    # Sidebar for model selection
    st.sidebar.header("Settings")
    model_choice = st.sidebar.selectbox(
        "Choose Prediction Model",
        ("SVM (Recommended)", "Random Forest", "Naive Bayes")
    )

    model_dict = {
        "Random Forest": rf_model,
        "SVM (Recommended)": svm_model,
        "Naive Bayes": nb_model
    }
    selected_model = model_dict[model_choice]

    # Main input area
    st.subheader("Select Symptoms")
    display_symptoms = [s.replace('_', ' ').capitalize() for s in symptoms_list]
    symptom_map = dict(zip(display_symptoms, symptoms_list))

    selected_display_symptoms = st.multiselect(
        "What symptoms are you experiencing?",
        options=display_symptoms
    )

    if st.button("Predict Disease"):
        if not selected_display_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            # Create input vector
            input_data = np.zeros(len(symptoms_list))
            for s in selected_display_symptoms:
                idx = symptoms_list.index(symptom_map[s])
                input_data[idx] = 1
            
            # Prediction
            prediction = selected_model.predict(input_data.reshape(1, -1))[0]
            
            # Display Result
            st.success(f"### Predicted Disease: **{prediction}**")
            st.write("---")
            st.write("**Symptoms analyzed:** " + ", ".join(selected_display_symptoms))

st.markdown("---")
st.markdown("Developed as a Machine Learning Project")
