# feedback.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def display_feedback_button():
    # Initialize a session state variable to toggle feedback form visibility
    if "feedback_visible" not in st.session_state:
        st.session_state.feedback_visible = False

    # Display the feedback button
    if st.button("Give Feedback"):
        st.session_state.feedback_visible = True

    # If the button was clicked, show the feedback form inside an expander
    if st.session_state.feedback_visible:
        with st.expander("Feedback Form", expanded=True):
            st.subheader("Feedback & Suggestions")
            with st.form("feedback_form"):
                name = st.text_input("Name (optional)")
                email = st.text_input("Email (optional)")
                outcome = st.selectbox("Did the prediction match your outcome?", ["Yes", "No", "Not Sure"])
                feedback_text = st.text_area("Your Feedback / Suggestions")
                submitted = st.form_submit_button("Submit Feedback")
                if submitted:
                    feedback_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name,
                        "Email": email,
                        "Outcome": outcome,
                        "Feedback": feedback_text
                    }
                    file_name = "feedback.csv"
                    if os.path.exists(file_name):
                        df = pd.read_csv(file_name)
                    else:
                        df = pd.DataFrame(columns=["Timestamp", "Name", "Email", "Outcome", "Feedback"])
                    
                    # Create a new DataFrame for the new row and concatenate
                    new_row = pd.DataFrame([feedback_data])
                    df = pd.concat([df, new_row], ignore_index=True)
                    
                    df.to_csv(file_name, index=False)
                    st.success("Thank you for your feedback!")
                    st.session_state.feedback_visible = False  # Hide form after submission
