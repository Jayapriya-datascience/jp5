import streamlit as st
import pickle
import numpy as np
import os

# Load Model and Scaler
def load_model_and_scaler():
    model_path = os.path.join("modeljp", "trained_modeljp.pkl")
    scaler_path = os.path.join("modeljp", "scalerjp.pkl")
    
    if not os.path.exists(model_path):
        st.error(f"❌ Model file not found! Expected at: {model_path}")
        st.stop()
    
    if not os.path.exists(scaler_path):
        st.error(f"❌ Scaler file not found! Expected at: {scaler_path}")
        st.stop()
    
    with open(model_path, "rb") as model_file:
        model=pickle.load(model_file)
        
    with open(scaler_path, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    
    return model, scaler
    # Make sure to call the function here, outside of the function definition.
    model, scaler = load_model_and_scaler()
    st.title("💤 Sleep Disorder Prediction App")

# Personal Info
st.title("Personal Info")
age = st.number_input("Age", min_value=10, max_value=100, value=25)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
gender_mapping = {"Male": 0, "Female": 1, "Other": 2}
gender_value = gender_mapping[gender]

occupation = st.selectbox("Occupation", ["Nurse", "Doctor", "Engineer", "Lawyer", "Teacher", "Accountant", "Salesperson", "Student", "Others"])
occupation_mapping = {"Nurse": 0, "Doctor": 1, "Engineer": 2, "Lawyer": 3, "Teacher": 4, "Accountant": 5, "Salesperson": 6, "Student": 7, "Others": 8}
occupation_value = occupation_mapping[occupation]

height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)

if height > 0 and weight > 0:
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        bmi_category = 0
    elif 18.5 <= bmi < 24.9:
        bmi_category = 1
    elif 25 <= bmi < 29.9:
        bmi_category = 2
    else:
        bmi_category = 3
    st.text_input("BMI Category", value=["Underweight", "Normal", "Overweight", "Obese"][bmi_category], disabled=True)

# Sleep Details
st.title("💤Sleep Details")
sleep_duration = st.slider("Sleep Duration (hours)", 1.0, 12.0, 7.0)
quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 5, key="quality_of_sleep")
st.session_state.sleep_details = {'quality_of_sleep': quality_of_sleep}  # Store it in session state
st.write()
st.markdown("""
<div style="color:orange;">
Quality of Sleep (1-10)<br>
- 1-3: Poor Sleep Quality (Frequent disturbances)  <br>
- 4-6: Fair Sleep Quality (Light sleep, not refreshing)  <br>
- 7-8: Good Sleep Quality (Mostly uninterrupted, refreshing)  <br>
- 9-10: Excellent Sleep Quality (Deep, restorative sleep)  
</div>
""", unsafe_allow_html=True)

physical_activity = st.slider("Physical Activity Level (0-100)", 0, 100, 30)
st.write()
st.write("""
<div style="color:orange;">
Physical Activity Level (Rating 0-100)<br>
- 0: No Physical Activity  <br>
- 10-30: Low Activity (Sedentary)<br>  
- 31-60: Moderate Activity (Light exercise)<br>  
- 61-80: High Activity (Regular exercise)  <br>
- 81-100: Very High Activity (Intense daily exercise) 
</div>
""", unsafe_allow_html=True)

# Health Details
st.title("Health Details")
stress_level = st.slider("Stress Level (0-10)", 0, 10, 5)
st.write()
st.write("""
<div style="color:orange;">
Stress Level (0-10)<br>
- 0: No Stress <br> 
- 1-3: Low Stress  <br>
- 4-6: Moderate Stress<br>  
- 7-8: High Stress  <br>
- 9-10: Extreme Stress  
</div>
""", unsafe_allow_html=True)

heart_rate = st.number_input("Heart Rate (bpm)", 40, 120, value=70)
daily_steps = st.number_input("Daily Steps(1-10000)", 0, 10000, value=5000, step=100)
st.write()
st.write("""
<div style="color:orange;">
Daily Steps : The average number of steps the individual takes per day
</div>
""", unsafe_allow_html=True)

systolic = st.number_input("Systolic Blood Pressure", 80, 200, value=120)
st.write()
st.write("""
<div style="color:orange;">
Systolic : The systolic blood pressure of the individual in mmHg.
</div>
""", unsafe_allow_html=True)


diastolic = st.number_input("Diastolic Blood Pressure", 50, 130, value=80)
st.write()
st.write("""
<div style="color:orange;">
Diastolic:The diastolic blood pressure of the individual in mmHg.
</div>
""", unsafe_allow_html=True)

# Predict Button Styling
st.markdown("""
    <style>
    div.stButton > button {
        background-color: green;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Sleep Disorders Information
disorder_info = {
    "Insomnia": ("Difficulty falling or staying asleep.", "Reduce caffeine, maintain a sleep schedule, try relaxation techniques."),
    "Sleep Anxiety": ("Anxiety-related sleep disturbances.", "Practice meditation, avoid screens before bed, deep breathing exercises."),
    "Obstructive Sleep Apnea": ("Breathing stops during sleep due to airway blockage.", "Lose weight, avoid alcohol, consider CPAP therapy."),
    "Hypertension-related Sleep Issues": ("Poor sleep linked to high blood pressure.", "Monitor BP, reduce salt, maintain a balanced diet."),
    "Restless Leg Syndrome": ("Uncontrollable urge to move legs, worse at night.", "Exercise, avoid caffeine, maintain a regular sleep schedule."),
    "Narcolepsy": ("Excessive daytime sleepiness, sudden sleep attacks.", "Maintain a consistent schedule, avoid heavy meals before bed."),
}

# Prediction Button
if st.button("Predict"):
    prediction = model.predict(input_features)
    input_features = np.array([[
        age, gender_value, occupation_value, sleep_duration, quality_of_sleep, 
        physical_activity, stress_level, bmi_category, heart_rate, 
        daily_steps, systolic, diastolic
    ]])
    
    input_features = scaler.transform(input_features)
    if prediction[0] == 1:
        st.error("⚠️ High risk of sleep disorder detected! Consult a doctor.")

        # Suggest possible disorders based on inputs
        possible_disorders = []
        
        if sleep_duration < 5 or quality_of_sleep < 3:
            possible_disorders.append("Insomnia")
        
        if stress_level > 7:
            possible_disorders.append("Sleep Anxiety")
        
        if bmi_category == 3 and heart_rate > 90:
            possible_disorders.append("Obstructive Sleep Apnea")
        
        if systolic > 140 or diastolic > 90:
            possible_disorders.append("Hypertension-related Sleep Issues")
        
        if daily_steps < 3000 and physical_activity < 20:
            possible_disorders.append("Restless Leg Syndrome")
        
        if sleep_duration > 9 and stress_level < 3:
            possible_disorders.append("Narcolepsy")

        if not possible_disorders:
            possible_disorders.append("General Sleep Disorder")

        st.warning(f"🛏️ **Possible Sleep Disorders:** {', '.join(possible_disorders)}")

        for disorder in possible_disorders:
            if disorder in disorder_info:
                st.subheader(f"🩺 {disorder}")
                st.write(f"🔹 **Definition:** {disorder_info[disorder][0]}")
                st.write(f"💡 **Tips:** {disorder_info[disorder][1]}")

    else:
        st.success("✅ No disease detected! Keep maintaining good habits!")
        st.subheader("🛌 Tips for Healthy Sleep")
        st.write("1. **Maintain a Consistent Sleep Schedule** – Go to bed and wake up at the same time every day, even on weekends.")
        st.write("2. **Create a Relaxing Bedtime Routine** – Avoid screens, heavy meals, and caffeine before bed. Try reading or meditation.")
        st.write("3. **Stay Physically Active** – Engage in regular exercise, but avoid intense workouts close to bedtime.")
        st.write("4. **Optimize Your Sleep Environment** – Keep your room dark, quiet, and cool for better sleep quality.")
        st.write("5. **Manage Stress and Anxiety** – Practice relaxation techniques like deep breathing, yoga, or journaling to reduce stress before sleep.")



st.write("📌 **Note:** This AI prediction should not replace professional medical advice.")
