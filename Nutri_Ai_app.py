# nutri_ai_app.py

import os
import re
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# -------------------------------
# 1. Setup
# -------------------------------
st.set_page_config(page_title="NutriAI - Indian Dietician", page_icon="🍛", layout="centered")

st.title("🍛 NutriAI – Your Indian Diet Assistant")
st.markdown("Namaste 🙏 I am NutriAI, your personalized Indian dietician.")

# Load API key securely from Streamlit Secrets
api_key = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0.2)

# -------------------------------
# 2. User Input Form
# -------------------------------
with st.form("user_form"):
    name = st.text_input("👤 Name")
    age = st.number_input("🎂 Age", min_value=1, max_value=100, value=25)
    gender = st.selectbox("⚧️ Gender", ["male", "female", "other"])
    goal = st.selectbox("🏁 Health Goal", ["Weight Loss", "Weight Gain", "Balanced Diet"])
    preference = st.selectbox("🌿 Diet Preference", ["veg", "non-veg", "vegan"])
    region = st.text_input("🍛 Preferred Indian Cuisine Region (e.g., South, North, West)")
    health_issue = st.text_input("🩺 Health Issues (PCOS, acne, thyroid, etc.)")
    height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=165)
    weight = st.number_input("⚖️ Weight (kg)", min_value=20, max_value=200, value=65)
    activity_level = st.selectbox("🏃 Activity Level", ["low", "moderate", "high"])

    submitted = st.form_submit_button("Generate Plan")

if not submitted:
    st.stop()

# -------------------------------
# 3. Generate Diet Plan
# -------------------------------
soft = "Prefer soft/easy-to-digest foods." if age > 50 else ""
prompt = f"Namaste {name}! I am NutriAI, your Indian dietician. Goal: {goal}. Age: {age}, Gender: {gender}, Region: {region}, Diet: {preference}, Health Issues: {health_issue}. {soft} Suggest a full day's meal plan with traditional Indian foods."

plan = llm.invoke([HumanMessage(content=prompt)]).content.strip()

st.subheader("🍽️ Personalized Diet Plan")
st.write(plan)

# -------------------------------
# 4. Nutrition Summary
# -------------------------------
bmr = 10 * weight + 6.25 * height - 5 * age
bmr += -161 if gender == "female" else 5
factor = {"low": 1.2, "moderate": 1.55, "high": 1.725}[activity_level]
calories = round(bmr * factor)
protein = round(weight * 1.2)

st.subheader("📊 Daily Nutrition Goal")
st.info(f"Calories: {calories} kcal | Protein: {protein} g")

# -------------------------------
# 5. Meal Logging
# -------------------------------
st.subheader("🧾 Meal Log")
breakfast = st.text_input("🍳 Breakfast")
lunch = st.text_input("🥗 Lunch")
dinner = st.text_input("🍲 Dinner")
snacks = st.text_input("🍪 Snacks")

if st.button("Analyze Meals"):
    meal_summary = f"""
    Breakfast: {breakfast}
    Lunch: {lunch}
    Dinner: {dinner}
    Snacks: {snacks}
    """
    response = llm.invoke([HumanMessage(content=f"Estimate total calories and protein for:\n{meal_summary}\nFormat: Calories: X kcal, Protein: Y g")])
    meal_analysis = response.content.strip()
    st.write("📋 Nutritional Analysis")
    st.success(meal_analysis)

    # Extract numbers
    cal = re.search(r'Calories\D+(\d+)', meal_analysis)
    prot = re.search(r'Protein\D+(\d+)', meal_analysis)
    consumed_cal = int(cal.group(1)) if cal else 0
    consumed_prot = int(prot.group(1)) if prot else 0
    remaining_cal = max(calories - consumed_cal, 0)
    remaining_prot = max(protein - consumed_prot, 0)

    st.subheader("📉 Remaining Today")
    st.warning(f"Calories left: {remaining_cal} kcal | Protein left: {remaining_prot} g")

    # Progress Bar Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4))

    # Calories
    ax1.bar(["Goal","Consumed","Remaining"], [calories, consumed_cal, remaining_cal],
            color=["#4CAF50","#FF9800","#2196F3"])
    ax1.set_title("Calories Progress")
    ax1.set_ylabel("Calories (kcal)")
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # Protein
    ax2.bar(["Goal","Consumed","Remaining"], [protein, consumed_prot, remaining_prot],
            color=["#9C27B0","#FF5722","#03A9F4"])
    ax2.set_title("Protein Progress")
    ax2.set_ylabel("Protein (g)")
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(fig)

    # -------------------------------
    # 6. Exercise Suggestion
    # -------------------------------
    exercise_prompt = f"Suggest a short Indian home workout (yoga included) for Goal: {goal}, Gender: {gender}, Age: {age}, Health: {health_issue}"
    exercise = llm.invoke([HumanMessage(content=exercise_prompt)]).content.strip()
    st.subheader("🏃 Exercise Recommendation")
    st.write(exercise)

    # -------------------------------
    # 7. Export PDF
    # -------------------------------
    if st.button("📥 Download PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"NutriAI Health Report for {name}", ln=True, align='C')
        pdf.ln(10)

        pdf.multi_cell(0, 10, txt=f"""
        Name: {name}
        Age: {age}
        Gender: {gender}
        Goal: {goal}
        Diet: {preference}
        Region: {region}
        Health Issue: {health_issue}
        Height: {height} cm
        Weight: {weight} kg
        Activity: {activity_level}
        """)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Nutrition Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"Calories Needed: {calories} kcal\nProtein Needed: {protein} g")

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Diet Plan", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=plan)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Meal Log", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=meal_summary)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Nutritional Analysis", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=meal_analysis)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Exercise Recommendation", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=exercise)

        pdf.output("NutriAI_Report.pdf")
        with open("NutriAI_Report.pdf", "rb") as f:
            st.download_button("Download NutriAI_Report.pdf", f, file_name="NutriAI_Report.pdf", mime="application/pdf")
