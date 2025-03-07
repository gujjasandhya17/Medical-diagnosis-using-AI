import streamlit as st

def get_chatbot_response(user_message):
    """
    Returns a response based on keyword matching for various medical terms.
    Extend these rules as needed.
    """
    message = user_message.lower()
    
    # EHR related
    if "ehr" in message or "electronic health record" in message:
        return ("EHR stands for Electronic Health Record. It is a digital version of a patient's paper chart that "
                "contains medical history, diagnoses, medications, treatment plans, and other health information. "
                "EHRs enable real-time access to patient data, which improves the quality and efficiency of care.")
    
    # Diabetes Prediction terms
    elif "glucose" in message:
        return ("Glucose is the primary sugar found in your blood. Abnormal levels can indicate diabetes, "
                "and it is a key parameter in our diabetes prediction model.")
    elif "bmi" in message:
        return ("BMI stands for Body Mass Index. It is calculated using your height and weight to determine if you're within a healthy range, "
                "and is important in assessing diabetes risk.")
    elif "diabetes pedigree" in message:
        return ("The Diabetes Pedigree Function estimates the genetic predisposition for diabetes based on family history, "
                "and is used to improve prediction accuracy.")
    elif "insulin" in message:
        return ("Insulin is a hormone produced by the pancreas that regulates blood sugar levels. In diabetes prediction, "
                "measured insulin levels can help determine how well the body is managing glucose.")
    
    # Heart Disease Prediction terms
    elif "cholesterol" in message:
        return ("Cholesterol is a fatty substance in the blood. High levels of LDL (bad cholesterol) can increase the risk "
                "of heart disease, which is why it's an important factor in our heart disease prediction model.")
    elif "resting blood pressure" in message or "trestbps" in message:
        return ("Resting Blood Pressure is the pressure in your arteries when your heart is at rest. Elevated levels can be a risk factor for heart disease.")
    elif "chest pain" in message or "cp" in message:
        return ("Chest pain is a key symptom in heart disease prediction. The model distinguishes between different types such as typical angina, atypical angina, non-anginal pain, and asymptomatic chest pain.")
    elif "fasting blood sugar" in message or "fbs" in message:
        return ("Fasting Blood Sugar measures your blood glucose after a period of fasting. It is used to assess the risk of both diabetes and heart disease.")
    elif "thal" in message:
        return ("Thalassemia (denoted as 'thal' in the model) refers to certain blood disorder indicators that can contribute to heart disease risk assessment.")
    
    # Parkinson's Prediction terms
    elif "mdvp" in message:
        return ("MDVP stands for Multi-Dimensional Voice Program. It measures various voice parameters such as fundamental frequency (Fo), "
                "maximum frequency (Fhi), and minimum frequency (Flo) which are used in predicting Parkinson's disease.")
    elif "jitter" in message:
        return ("Jitter measures the frequency variation in the voice signal. Increased jitter is often associated with vocal instability in Parkinson's disease.")
    elif "shimmer" in message:
        return ("Shimmer measures the amplitude variation in the voice. Changes in shimmer can indicate issues with vocal cord function, which are used in Parkinson's prediction.")
    
    # Lung Cancer Prediction terms
    elif "smoking" in message:
        return ("Smoking is a major risk factor for lung cancer. Our lung cancer prediction model takes smoking history into account "
                "along with other symptoms to assess risk.")
    elif "peer pressure" in message:
        return ("Peer pressure can influence habits like smoking, which in turn affect lung cancer risk. It is one of the social factors considered.")
    
    # Hypo-Thyroid Prediction terms
    elif "tsh" in message:
        return ("TSH stands for Thyroid Stimulating Hormone. It regulates thyroid function, and abnormal levels can indicate hypo-thyroidism.")
    elif "t3" in message:
        return ("T3, or triiodothyronine, is an active thyroid hormone. Its level helps in evaluating thyroid function in hypo-thyroid prediction.")
    elif "tt4" in message:
        return ("TT4 stands for Total Thyroxine, which is a measure of the thyroid hormone thyroxine in the blood. It is used in assessing thyroid function.")
    elif "thyroxine" in message:
        return ("Being on thyroxine indicates that a patient is receiving thyroid hormone replacement therapy, "
                "which is essential in managing hypo-thyroidism.")
    
    # Dynamic What-If Analysis and Interactive Tutorials
    elif "what-if" in message or "dynamic what-if" in message:
        return ("Dynamic What-If Analysis is an interactive feature that allows you to modify input parameters and observe how those changes affect the prediction outcomes.")
    elif "tutorial" in message:
        return ("Interactive Tutorials provide step-by-step guidance on how to use the system, understand your predictions, and learn more about medical concepts.")
    
    # Generic fall-back for common questions
    elif "what" in message or "how" in message:
        return ("You can enter your health data in the respective sections on the dashboard. "
                "If you have any further questions about disease predictions or medical terms, feel free to ask!")
    
    else:
        return "I'm here to help! Could you please elaborate on your question or specify a topic?"

def display_chatbot():
    """
    Displays the virtual assistant in the sidebar using a form for immediate responses.
    """
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.sidebar.markdown("### 🤖 Virtual Assistant")
    
    # Chat input form using Streamlit form for immediate submission
    with st.sidebar.form(key='chat_form'):
        user_input = st.text_input("Your question:")
        submit = st.form_submit_button("Send")
        if submit and user_input:
            response = get_chatbot_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Assistant", response))
    
    # Optionally, a button to clear the conversation
    if st.sidebar.button("Clear Chat"):
        st.session_state.chat_history = []
    
    # Display the conversation history
    st.sidebar.markdown("#### Conversation History")
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.sidebar.markdown(f"**You:** {message}")
        else:
            st.sidebar.markdown(f"**Assistant:** {message}")
