# tutorials.py
import streamlit as st

def display_tutorials():
    st.header("Interactive Tutorials & Onboarding")
    st.markdown("Welcome! This guide will help you understand each input parameter and how it affects the predictions. Click on each section for more details.")

    with st.expander("Diabetes Prediction Tutorial"):
        st.subheader("Diabetes Prediction")
        st.markdown("""
        **Overview:**  
        Diabetes prediction uses various health parameters such as glucose level, BMI, blood pressure, etc., to assess the risk of diabetes.
        """)
        st.video("https://youtu.be/gGLofmo7q2E?si=UJjQ_1jhvc6I2-94")  # Replace with your actual video URL or file path
        st.markdown("""
        **Key Parameters:**  
        - **Glucose Level:** Indicates blood sugar levels.  
        - **BMI:** Body Mass Index helps assess obesity risk.  
        - **Blood Pressure:** High values can be a risk factor.
        """)

    with st.expander("Heart Disease Prediction Tutorial"):
        st.subheader("Heart Disease Prediction")
        st.markdown("""
        **Overview:**  
        Heart disease prediction involves parameters like age, cholesterol, blood pressure, and ECG results to determine the likelihood of heart conditions.
        """)
        st.video("https://youtu.be/KPKLq-LQjbc?si=nzrfKzKCv9bbns-Q")  # Replace with your actual video URL or file path
        st.markdown("""
        **Key Parameters:**  
        - **Chest Pain Type:** Indicates the type of chest pain experienced.  
        - **Resting Blood Pressure:** Helps assess cardiovascular health.  
        - **Cholesterol Level:** Elevated cholesterol is a risk factor.
        """)

    with st.expander("Parkinson's Disease Prediction Tutorial"):
        st.subheader("Parkinson's Disease Prediction")
        st.markdown("""
        **Overview:**  
        Parkinson's prediction uses voice measurements and other neurological parameters to detect early signs of the disease.
        """)
        st.video("https://youtu.be/nDLKGrxthag?si=T1cnumYAAow4SFNe")  # Replace with your actual video URL or file path
        st.markdown("""
        **Key Parameters:**  
        - **MDVP:Fo(Hz):** Fundamental frequency of voice.  
        - **Jitter:** Measures variations in voice frequency.  
        - **Shimmer:** Measures variations in voice amplitude.
        """)

    with st.expander("Lung Cancer Prediction Tutorial"):
        st.subheader("Lung Cancer Prediction")
        st.markdown("""
        **Overview:**  
        Lung cancer prediction incorporates lifestyle factors and symptoms like smoking habits, cough, and breath issues to assess cancer risk.
        """)
        st.video("https://youtu.be/6moQ47RsgYg?si=LYIR-czCMS8TGzl3")  # Replace with your actual video URL or file path
        st.markdown("""
        **Key Parameters:**  
        - **Smoking:** A major risk factor.  
        - **Chronic Disease:** History of respiratory conditions.  
        - **Coughing & Breathlessness:** Common symptoms.
        """)

    with st.expander("Hypo-Thyroid Prediction Tutorial"):
        st.subheader("Hypo-Thyroid Prediction")
        st.markdown("""
        **Overview:**  
        Hypo-Thyroid prediction analyzes thyroid hormone levels, TSH, and clinical symptoms to determine thyroid function.
        """)
        st.video("https://youtu.be/wyanDtvx8K0?si=rnz8qWBNUdbjfsoy")  # Replace with your actual video URL or file path
        st.markdown("""
        **Key Parameters:**  
        - **TSH Level:** Indicator of thyroid function.  
        - **T3 and TT4 Levels:** Essential thyroid hormones.  
        - **On Thyroxine:** Indicates if the patient is on thyroid medication.
        """)

