import streamlit as st# type: ignore # Set page configuration with title and icon
import pickle
import csv
import os
from datetime import datetime
import pandas as pd # type: ignore
import wearable_integration
import what_if_analysis
import tutorials
import feedback
import chatbot
import sqlite3
from user_auth import user_authentication

st.set_page_config(page_title="Healix", page_icon="🧬")

# 🔒 Ensure user authentication before accessing the app
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_name"] = None

if not st.session_state["logged_in"]:
    user_authenticated = user_authentication()
    if not user_authenticated:
        st.stop()  # Stop app execution until the user logs in


from streamlit_option_menu import option_menu # type: ignore

chatbot.display_chatbot()

with st.sidebar:
    
    styles={
            "container": {"padding": "5px", "background-color": "rgba(0,0,0,0.5)"},
            "icon": {"color": "white", "font-size": "25px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#527ade"},
            "nav-link-selected": {"background-color": "#527ade"},
        }

# Logout Button
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["user_name"] = None
    st.success("🔓 Logged out successfully!")
    st.rerun()


# Custom CSS styling to create a unique UI/UX
custom_css = """
<style>
/* Set a unique background image with full cover and an overlay for readability */
[data-testid="stAppViewContainer"] {
    background-image: url("https://your-unique-image-url.com/your-image.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
}

/* Overlay to darken/lighten background for better contrast */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);  /* Adjust transparency as needed */
    z-index: 0;
}

/* Ensure your main content appears above the overlay */
[data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 1;
}

/* Custom font, color, and text styling */
body {
    font-family: 'Montserrat', sans-serif;
}
h1, h2, h3, h4, h5, h6 {
    color: #1f4068;  /* Unique color for headings */
}

/* Custom styling for buttons */
.stButton > button {
    background-color: #1f4068;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
}
.stButton > button:hover {
    background-color: #15315b;
}

/* Adjust other elements as desired */
</style>
"""


# Hide default Streamlit menu and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Adding Background Image with overlay
background_image_url = "https://media-hosting.imagekit.io//4b80d9c2cbee4633/medicoai%20pic_cleanup.PNG?Expires=1835722284&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=LDPpcc-0f0HPSvc4rIBaeu7FyXVWBP8HDPtVRrqE3Zfd58Mg~RL5TVs6K9wVBnlYjd6rIyFkYSGq5lbSFzXgnYDxgjqIsNYLzPyE1bOro51o1Hml4jL9ECRHUGkZAV6HFoVnJrXOrowYx0sPEsZQY5nui9hhCF3o8kamHY5XjjTrNOPvPAEm8FYtXedX4tlyj-OE3biKT7JAJf1HeGktFZ2FfQUnVRGx3D6UodhXPK8W7n01DJkAfu6QM6kiOeWIamlTHqtdbMzhUU875art0FpibZ6P8t0fSaeycXICXPTxXdAgQm0BvwfUNl5v1Iy-pj4vfci2mCtNb1E3YUT-pQ__"
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url({background_image_url});
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
}}
/* Added transitions for smoother UI interactions */
.stButton button {{
    transition: transform 0.3s ease;
}}
.stButton button:hover {{
    transform: scale(1.05);
}}
input, button {{
    transition: all 0.3s ease-in-out;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the saved models
models = {
    'diabetes': pickle.load(open('Models/diabetes_model.sav', 'rb')),
    'heart_disease': pickle.load(open('Models/heart_disease_model.sav', 'rb')),
    'parkinsons': pickle.load(open('Models/parkinsons_model.sav', 'rb')),
    'lung_cancer': pickle.load(open('Models/lungs_disease_model.sav', 'rb')),
    'thyroid': pickle.load(open('Models/Thyroid_model.sav', 'rb'))
}

# Helper function to log prediction results
def log_result(disease, inputs, result):
    filename = "prediction_log.csv"
    header = ["Timestamp", "Disease", "Inputs", "Result"]
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), disease, inputs, result])

# ------------------ Landing Page Logic ------------------
if 'visited' not in st.session_state:
    st.session_state.visited = False

def mark_visited():
    st.session_state.visited = True

if not st.session_state.visited:
    st.markdown("<h1 style='font-family: Montserrat; color: #9EB7B9; text-align: center;'>Medical Diagnosis System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: Montserrat; text-align: center;'>Welcome to the Multiple Disease Prediction</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-family: Montserrat; text-align: center;'>This system integrates various models to predict diseases such as Diabetes, Heart Disease, Parkinson's, Lung Cancer, and Hypo-Thyroid disease. Explore advanced features like wearable integration, dynamic what-if analysis. Click the button below to get started.</p>",
        unsafe_allow_html=True
    )
    
    st.button("Enter", on_click=mark_visited)
    st.markdown("""
    <div class="health-quote">
    <p style="position:fixed; bottom: 0; width: 100%; font-family: 'Arial', Courier, monospace; font-size: 18px; color: #FFFFFF;">
        "Health is the greatest gift, contentment the greatest wealth, faithfulness the best relationship." - Buddha
    </p>
</div>

    """, unsafe_allow_html=True)
    st.stop()

# ------------------ Main Navigation ------------------

# Extend the navigation selectbox to include new engagement features
selected = st.selectbox(
    'Select a Feature',
    ['Diabetes Prediction',
     'Heart Disease Prediction',
     'Parkinsons Prediction',
     'Lung Cancer Prediction',
     'Hypo-Thyroid Prediction',
     'Dynamic What-If Analysis',
     'Interactive Tutorials']
)



# Wearable Integration: Add a section in the sidebar
st.sidebar.header("Wearable Device Integration")
api_token = st.sidebar.text_input("Enter your API Token", type="password")
if st.sidebar.button("Sync Wearable Data"):
    wearable_data = wearable_integration.fetch_wearable_data(api_token)
    if wearable_data:
        st.sidebar.success("Data fetched successfully!")
        st.sidebar.write("Resting Heart Rate:", wearable_data['heart_rate'])
    else:
        st.sidebar.error("Failed to fetch data. Please check your API token.")


# Routing to new engagement features or disease predictions based on selection
if selected == 'Dynamic What-If Analysis':
    what_if_analysis.display_what_if_analysis()


elif selected == 'Interactive Tutorials':
    tutorials.display_tutorials()



# -------------------- Diabetes Prediction --------------------
elif selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction')
    st.write("Enter the following details to predict diabetes:")
    with st.expander("Enter Diabetes Details"):
        st.info("FAQ: 'Glucose Level' is measured in mg/dl, and 'BMI' is the Body Mass Index. Ensure you enter realistic clinical values.")
        Pregnancies = st.number_input('Number of Pregnancies', key='Pregnancies', help='Enter the number of times the person has been pregnant.', step=1)
        Glucose = st.number_input('Glucose Level', key='Glucose', help='Enter the blood glucose level (mg/dl).', step=1)
        BloodPressure = st.number_input('Blood Pressure', key='BloodPressure', help='Enter the resting blood pressure (mm Hg).', step=1)
        SkinThickness = st.number_input('Skin Thickness', key='SkinThickness', help='Enter the skin thickness value (mm).', step=1)
        Insulin = st.number_input('Insulin Level', key='Insulin', help='Enter the insulin level (mu U/ml).', step=1)
        BMI = st.number_input('BMI', key='BMI', help='Enter the Body Mass Index value (kg/m²).', step=1)
        DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function', key='DiabetesPedigreeFunction', help='Enter the diabetes pedigree function value.', step=1)
        Age = st.number_input('Age', key='Age', help='Enter the age of the person in years.', step=1)
    if st.button('Diabetes Test Result'):
        with st.spinner("Processing Diabetes Prediction..."):
            diab_prediction = models['diabetes'].predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
        st.success(diab_diagnosis)
        inputs = {
            "Pregnancies": Pregnancies,
            "Glucose": Glucose,
            "BloodPressure": BloodPressure,
            "SkinThickness": SkinThickness,
            "Insulin": Insulin,
            "BMI": BMI,
            "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
            "Age": Age
        }
        log_result("Diabetes", inputs, diab_diagnosis)

# -------------------- Heart Disease Prediction --------------------
elif selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction')
    st.write("Enter the following details to predict heart disease:")
    with st.expander("Enter Heart Disease Details"):
        st.info("FAQ: Select categorical inputs using dropdowns. For 'Chest Pain Type', typical angina is 0, atypical angina is 1, non-anginal pain is 2, and asymptomatic is 3.")
        age = st.number_input('Age', key='age', help='Enter the age in years.', step=1)
        sex = st.selectbox('Sex', options=["Male", "Female"], key='sex', help='Select the gender (Male=1, Female=0).')
        sex = 1 if sex == "Male" else 0
        cp = st.selectbox('Chest Pain Type', options=["Typical Angina (0)", "Atypical Angina (1)", "Non-Anginal Pain (2)", "Asymptomatic (3)"], key='cp', help='Select the chest pain type.')
        mapping_cp = {"Typical Angina (0)": 0, "Atypical Angina (1)": 1, "Non-Anginal Pain (2)": 2, "Asymptomatic (3)": 3}
        cp = mapping_cp[cp]
        trestbps = st.number_input('Resting Blood Pressure', key='trestbps', help='Enter resting blood pressure (mm Hg).', step=1)
        chol = st.number_input('Serum Cholesterol', key='chol', help='Enter serum cholesterol (mg/dl).', step=1)
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', options=["Yes", "No"], key='fbs', help='Select whether fasting blood sugar is greater than 120 mg/dl.')
        fbs = 1 if fbs == "Yes" else 0
        restecg = st.selectbox('Resting ECG Results', options=["Normal (0)", "ST-T wave abnormality (1)", "Left ventricular hypertrophy (2)"], key='restecg', help='Select the resting ECG result.')
        mapping_ecg = {"Normal (0)": 0, "ST-T wave abnormality (1)": 1, "Left ventricular hypertrophy (2)": 2}
        restecg = mapping_ecg[restecg]
        thalach = st.number_input('Maximum Heart Rate Achieved', key='thalach', help='Enter the maximum heart rate achieved (bpm).', step=1)
        exang = st.selectbox('Exercise Induced Angina', options=["Yes", "No"], key='exang', help='Select whether exercise induces angina.')
        exang = 1 if exang == "Yes" else 0
        oldpeak = st.number_input('ST Depression', key='oldpeak', help='Enter ST depression induced by exercise.', step=1)
        slope = st.selectbox('Slope of Peak Exercise ST Segment', options=["Upsloping (0)", "Flat (1)", "Downsloping (2)"], key='slope', help='Select the slope.')
        mapping_slope = {"Upsloping (0)": 0, "Flat (1)": 1, "Downsloping (2)": 2}
        slope = mapping_slope[slope]
        ca = st.slider('Major Vessels Colored by Fluoroscopy', min_value=0, max_value=3, key="ca", help="Select the number of major vessels (0-3) colored by fluoroscopy.")
        thal = st.selectbox('Thalassemia', options=["Normal (0)", "Fixed defect (1)", "Reversible defect (2)"], key='thal', help='Select thalassemia status.')
        mapping_thal = {"Normal (0)": 0, "Fixed defect (1)": 1, "Reversible defect (2)": 2}
        thal = mapping_thal[thal]
    if st.button('Heart Disease Test Result'):
        with st.spinner("Processing Heart Disease Prediction..."):
            heart_prediction = models['heart_disease'].predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            heart_diagnosis = 'The person has heart disease' if heart_prediction[0] == 1 else 'The person does not have heart disease'
        st.success(heart_diagnosis)
        inputs = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal
        }
        log_result("Heart Disease", inputs, heart_diagnosis)

# -------------------- Parkinson's Prediction --------------------
elif selected == "Parkinsons Prediction":
    st.title("Parkinson's Disease Prediction")
    st.write("Enter the following details to predict Parkinson's disease:")
    with st.expander("Enter Parkinson's Details"):
        st.info("FAQ: Values such as MDVP:Fo(Hz) represent voice frequency measures. Please consult your dataset documentation for units.")
        fo = st.number_input('MDVP:Fo(Hz)', key='fo', help='Enter the fundamental frequency in Hz.', step=1)
        fhi = st.number_input('MDVP:Fhi(Hz)', key='fhi', help='Enter the maximum vocal frequency in Hz.', step=1)
        flo = st.number_input('MDVP:Flo(Hz)', key='flo', help='Enter the minimum vocal frequency in Hz.', step=1)
        Jitter_percent = st.number_input('MDVP:Jitter(%)', key='Jitter_percent', help='Enter the jitter percentage.', step=1)
        Jitter_Abs = st.number_input('MDVP:Jitter(Abs)', key='Jitter_Abs', help='Enter the absolute jitter value.', step=1)
        RAP = st.number_input('MDVP:RAP', key='RAP', help='Enter the relative average perturbation.', step=1)
        PPQ = st.number_input('MDVP:PPQ', key='PPQ', help='Enter the pitch perturbation quotient.', step=1)
        DDP = st.number_input('Jitter:DDP', key='DDP', help='Enter the difference of differences of pitch.', step=1)
        Shimmer = st.number_input('MDVP:Shimmer', key='Shimmer', help='Enter the shimmer value.', step=1)
        Shimmer_dB = st.number_input('MDVP:Shimmer(dB)', key='Shimmer_dB', help='Enter the shimmer value in dB.', step=1)
        APQ3 = st.number_input('Shimmer:APQ3', key='APQ3', help='Enter the amplitude perturbation quotient (3).', step=1)
        APQ5 = st.number_input('Shimmer:APQ5', key='APQ5', help='Enter the amplitude perturbation quotient (5).', step=1)
        APQ = st.number_input('MDVP:APQ', key='APQ', help='Enter the amplitude perturbation quotient.', step=1)
        DDA = st.number_input('Shimmer:DDA', key='DDA', help='Enter the shimmer of DDA.', step=1)
        NHR = st.number_input('NHR', key='NHR', help='Enter the noise-to-harmonics ratio.', step=1)
        HNR = st.number_input('HNR', key='HNR', help='Enter the harmonics-to-noise ratio.', step=1)
        RPDE = st.number_input('RPDE', key='RPDE', help='Enter the recurrence period density entropy.', step=1)
        DFA = st.number_input('DFA', key='DFA', help='Enter the detrended fluctuation analysis value.', step=1)
        spread1 = st.number_input('Spread1', key='spread1', help='Enter spread1 value.', step=1)
        spread2 = st.number_input('Spread2', key='spread2', help='Enter spread2 value.', step=1)
        D2 = st.number_input('D2', key='D2', help='Enter the correlation dimension D2.', step=1)
        PPE = st.number_input('PPE', key='PPE', help='Enter the PPE value.', step=1)
    if st.button("Parkinson's Test Result"):
        with st.spinner("Processing Parkinson's Prediction..."):
            parkinsons_prediction = models['parkinsons'].predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]])
            parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
        st.success(parkinsons_diagnosis)
        inputs = {
            "fo": fo,
            "fhi": fhi,
            "flo": flo,
            "Jitter_percent": Jitter_percent,
            "Jitter_Abs": Jitter_Abs,
            "RAP": RAP,
            "PPQ": PPQ,
            "DDP": DDP,
            "Shimmer": Shimmer,
            "Shimmer_dB": Shimmer_dB,
            "APQ3": APQ3,
            "APQ5": APQ5,
            "APQ": APQ,
            "DDA": DDA,
            "NHR": NHR,
            "HNR": HNR,
            "RPDE": RPDE,
            "DFA": DFA,
            "spread1": spread1,
            "spread2": spread2,
            "D2": D2,
            "PPE": PPE
        }
        log_result("Parkinson's", inputs, parkinsons_diagnosis)

# -------------------- Lung Cancer Prediction --------------------
elif selected == "Lung Cancer Prediction":
    st.title("Lung Cancer Prediction")
    st.write("Enter the following details to predict lung cancer:")
    with st.expander("Enter Lung Cancer Details"):
        st.info("FAQ: For binary responses (Yes/No), select the appropriate option. Age should be in years.")
        GENDER = st.selectbox('Gender', options=["Male", "Female"], key='GENDER', help='Select the gender (Male=1, Female=0).')
        GENDER = 1 if GENDER == "Male" else 0
        AGE = st.number_input('Age', key='AGE', help='Enter the age in years.', step=1)
        SMOKING = st.selectbox('Smoking', options=["Yes", "No"], key='SMOKING', help='Does the person smoke? (Yes=1, No=0).')
        SMOKING = 1 if SMOKING == "Yes" else 0
        YELLOW_FINGERS = st.selectbox('Yellow Fingers', options=["Yes", "No"], key='YELLOW_FINGERS', help='Does the person have yellow fingers? (Yes=1, No=0).')
        YELLOW_FINGERS = 1 if YELLOW_FINGERS == "Yes" else 0
        ANXIETY = st.selectbox('Anxiety', options=["Yes", "No"], key='ANXIETY', help='Does the person experience anxiety? (Yes=1, No=0).')
        ANXIETY = 1 if ANXIETY == "Yes" else 0
        PEER_PRESSURE = st.selectbox('Peer Pressure', options=["Yes", "No"], key='PEER_PRESSURE', help='Is the person under peer pressure? (Yes=1, No=0).')
        PEER_PRESSURE = 1 if PEER_PRESSURE == "Yes" else 0
        CHRONIC_DISEASE = st.selectbox('Chronic Disease', options=["Yes", "No"], key='CHRONIC_DISEASE', help='Does the person have any chronic diseases? (Yes=1, No=0).')
        CHRONIC_DISEASE = 1 if CHRONIC_DISEASE == "Yes" else 0
        FATIGUE = st.selectbox('Fatigue', options=["Yes", "No"], key='FATIGUE', help='Does the person experience fatigue? (Yes=1, No=0).')
        FATIGUE = 1 if FATIGUE == "Yes" else 0
        ALLERGY = st.selectbox('Allergy', options=["Yes", "No"], key='ALLERGY', help='Does the person have allergies? (Yes=1, No=0).')
        ALLERGY = 1 if ALLERGY == "Yes" else 0
        WHEEZING = st.selectbox('Wheezing', options=["Yes", "No"], key='WHEEZING', help='Does the person experience wheezing? (Yes=1, No=0).')
        WHEEZING = 1 if WHEEZING == "Yes" else 0
        ALCOHOL_CONSUMING = st.selectbox('Alcohol Consuming', options=["Yes", "No"], key='ALCOHOL_CONSUMING', help='Does the person consume alcohol? (Yes=1, No=0).')
        ALCOHOL_CONSUMING = 1 if ALCOHOL_CONSUMING == "Yes" else 0
        COUGHING = st.selectbox('Coughing', options=["Yes", "No"], key='COUGHING', help='Does the person experience coughing? (Yes=1, No=0).')
        COUGHING = 1 if COUGHING == "Yes" else 0
        SHORTNESS_OF_BREATH = st.selectbox('Shortness Of Breath', options=["Yes", "No"], key='SHORTNESS_OF_BREATH', help='Does the person have shortness of breath? (Yes=1, No=0).')
        SHORTNESS_OF_BREATH = 1 if SHORTNESS_OF_BREATH == "Yes" else 0
        SWALLOWING_DIFFICULTY = st.selectbox('Swallowing Difficulty', options=["Yes", "No"], key='SWALLOWING_DIFFICULTY', help='Does the person have difficulty swallowing? (Yes=1, No=0).')
        SWALLOWING_DIFFICULTY = 1 if SWALLOWING_DIFFICULTY == "Yes" else 0
        CHEST_PAIN = st.selectbox('Chest Pain', options=["Yes", "No"], key='CHEST_PAIN', help='Does the person experience chest pain? (Yes=1, No=0).')
        CHEST_PAIN = 1 if CHEST_PAIN == "Yes" else 0
    if st.button("Lung Cancer Test Result"):
        with st.spinner("Processing Lung Cancer Prediction..."):
            lungs_prediction = models['lung_cancer'].predict([[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, FATIGUE, ALLERGY, WHEEZING, ALCOHOL_CONSUMING, COUGHING, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN]])
            lungs_diagnosis = "The person has lung cancer disease" if lungs_prediction[0] == 1 else "The person does not have lung cancer disease"
        st.success(lungs_diagnosis)
        inputs = {
            "GENDER": GENDER,
            "AGE": AGE,
            "SMOKING": SMOKING,
            "YELLOW_FINGERS": YELLOW_FINGERS,
            "ANXIETY": ANXIETY,
            "PEER_PRESSURE": PEER_PRESSURE,
            "CHRONIC_DISEASE": CHRONIC_DISEASE,
            "FATIGUE": FATIGUE,
            "ALLERGY": ALLERGY,
            "WHEEZING": WHEEZING,
            "ALCOHOL_CONSUMING": ALCOHOL_CONSUMING,
            "COUGHING": COUGHING,
            "SHORTNESS_OF_BREATH": SHORTNESS_OF_BREATH,
            "SWALLOWING_DIFFICULTY": SWALLOWING_DIFFICULTY,
            "CHEST_PAIN": CHEST_PAIN
        }
        log_result("Lung Cancer", inputs, lungs_diagnosis)

# -------------------- Hypo-Thyroid Prediction --------------------
elif selected == "Hypo-Thyroid Prediction":
    st.title("Hypo-Thyroid Prediction")
    st.write("Enter the following details to predict hypo-thyroid disease:")
    with st.expander("Enter Hypo-Thyroid Details"):
        st.info("FAQ: 'On Thyroxine' and 'T3 Measured' are binary inputs. Age is in years and TSH, T3, TT4 are measured in their respective clinical units.")
        age = st.number_input('Age', key='age_thyroid', help='Enter the age in years.', step=1)
        sex = st.selectbox('Sex', options=["Male", "Female"], key='sex_thyroid', help='Select the gender (Male=1, Female=0).')
        sex = 1 if sex == "Male" else 0
        on_thyroxine = st.selectbox('On Thyroxine', options=["Yes", "No"], key='on_thyroxine', help='Is the person on thyroxine? (Yes=1, No=0).')
        on_thyroxine = 1 if on_thyroxine == "Yes" else 0
        tsh = st.number_input('TSH Level', key='tsh', help='Enter the TSH level (mIU/L).', step=1)
        t3_measured = st.selectbox('T3 Measured', options=["Yes", "No"], key='t3_measured', help='Was the T3 level measured? (Yes=1, No=0).')
        t3_measured = 1 if t3_measured == "Yes" else 0
        t3 = st.number_input('T3 Level', key='t3', help='Enter the T3 level (ng/dL).', step=1)
        tt4 = st.number_input('TT4 Level', key='tt4', help='Enter the TT4 level (µg/dL).', step=1)
    if st.button("Thyroid Test Result"):
        with st.spinner("Processing Thyroid Prediction..."):
            thyroid_prediction = models['thyroid'].predict([[age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]])
            thyroid_diagnosis = "The person has Hypo-Thyroid disease" if thyroid_prediction[0] == 1 else "The person does not have Hypo-Thyroid disease"
        st.success(thyroid_diagnosis)
        inputs = {
            "age": age,
            "sex": sex,
            "on_thyroxine": on_thyroxine,
            "tsh": tsh,
            "t3_measured": t3_measured,
            "t3": t3,
            "tt4": tt4
        }
        log_result("Hypo-Thyroid", inputs, thyroid_diagnosis)

# Download Prediction Log if available
if os.path.exists("prediction_log.csv"):
    with open("prediction_log.csv", "rb") as log_file:
        st.sidebar.download_button("Download Prediction Log", log_file, "prediction_log.csv", "text/csv")

        # Add extra vertical space to push the feedback section to the bottom
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# Inject CSS to center the feedback section
st.markdown(
    """
    <style>
    .centered-feedback {
        text-align: center;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use a container to center the feedback button and form
with st.container():
    st.markdown('<div class="centered-feedback">', unsafe_allow_html=True)
    feedback.display_feedback_button()
    st.markdown('</div>', unsafe_allow_html=True)
#st.markdown(custom_css, unsafe_allow_html=True)

