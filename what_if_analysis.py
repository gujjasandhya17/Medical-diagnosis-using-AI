# what_if_analysis.py
import streamlit as st
import plotly.express as px
import pandas as pd

def display_what_if_analysis():
    """
    Renders an interactive 'What-If Analysis' section in your Streamlit app.
    Users can adjust parameters and see how their risk score changes.
    """
    st.header("Dynamic What-If Analysis")
    st.markdown("Adjust the sliders below to see how changes in lifestyle and health parameters might influence your risk profile.")

    # Interactive sliders for user input
    age = st.slider("Age", min_value=20, max_value=80, value=50)
    cholesterol = st.slider("Serum Cholesterol (mg/dl)", min_value=100, max_value=400, value=200)
    exercise = st.slider("Exercise Frequency (times per week)", min_value=0, max_value=7, value=3)
    smoking = st.selectbox("Smoking Habit", options=["Non-Smoker", "Smoker"], index=0)

    # Example risk calculation function (modify based on your actual logic)
    def calculate_risk(age, cholesterol, exercise, smoking):
        base_risk = 0.05 * age + 0.01 * cholesterol - 0.5 * exercise
        if smoking == "Smoker":
            base_risk += 10
        return base_risk

    current_risk = calculate_risk(age, cholesterol, exercise, smoking)
    st.write(f"Predicted Risk Score: {current_risk:.2f}")

    # Generate a line chart to show risk variation with age
    ages = list(range(20, 81))
    risks = [calculate_risk(a, cholesterol, exercise, smoking) for a in ages]
    df = pd.DataFrame({'Age': ages, 'Risk': risks})
    fig = px.line(df, x="Age", y="Risk", title="Risk Variation with Age")
    st.plotly_chart(fig)
