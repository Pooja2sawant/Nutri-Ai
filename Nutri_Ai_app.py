# STEP 0: Install dependencies
!pip install -qU google-generativeai==0.8.5 google-ai-generativelanguage==0.6.15 langgraph langchain langchain-google-genai openai matplotlib fpdf

# STEP 1: Imports and secure API key input
import os
import getpass
import matplotlib.pyplot as plt
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import re
from fpdf import FPDF

# STEP 2:Secure Gemini API Key input
os.environ['GOOGLE_API_KEY'] = getpass.getpass("Enter your Google API Key: ")

# STEP 3: Initialize Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0.2)
# STEP 4: Collect user data
def get_user_input(state: dict) -> dict:
    print("Namaste 🙏! I am NutriAI, your Indian dietician. Let's begin your health journey!")
    name = input("👤 What's your name? ")
    age = int(input("🎂 Your age: "))
    gender = input("⚧️ Your gender (male/female/other): ").strip().lower()
    goal = input("🏁 Your health goal? (weight loss/gain, healthy diet): ")
    preference = input("🌿 Diet preference (veg/non-veg/vegan): ")
    region = input("🍛 Preferred Indian cuisine region: ")
    health_issue = input("🩺 Any health issues? (PCOS, acne, thyroid, etc.): ")
    height = float(input("📏 Height in cm: ").strip())
    weight = float(input("⚖️ Weight in kg: ").strip())
    activity_level = input("🏃 Activity level (low, moderate, high): ").strip().lower()

    state.update({"name": name, "age": age, "gender": gender, "goal": goal, "preference": preference,
                  "region": region, "health_issue": health_issue, "height": height, "weight": weight,
                  "activity_level": activity_level})
    return state

# STEP 5: Classify goal
def classify_goal(state: dict) -> dict:
    goal = state['goal'].lower()
    if "loss" in goal:
        category = "Weight Loss"
    elif "gain" in goal:
        category = "Weight Gain"
    else:
        category = "Balanced Diet"
    print(f"🎯 Goal classified as: {category}")
    state["category"] = category
    return state

# STEP 6: Goal router
def diet_router(state: dict) -> str:
    cat = state["category"].lower()
    if "loss" in cat:
        return "loss"
    elif "gain" in cat:
        return "gain"
    return "balanced"

# STEP 7: Generate meal plan
def generate_plan(state: dict, goal_type: str) -> dict:
    soft = "Prefer soft/easy-to-digest foods." if state["age"] > 50 else ""
    prompt = f"Namaste {state['name']} 🙏! I am NutriAI, your Indian dietician. Let's create your Indian meal plan. Goal: {state['goal']} ({goal_type}) Age: {state['age']}, Gender: {state['gender']}, Region: {state['region']}, Diet: {state['preference']}, Health Issues: {state['health_issue']}. {soft} Suggest a full day's meal plan with traditional Indian foods."
    response = llm.invoke([HumanMessage(content=prompt)])
    state["plan"] = response.content.strip()
    print("\n🍽️ Your Personalized Diet Plan:\n")
    print(state["plan"])
    return state

def loss_node(state): return generate_plan(state, "Weight Loss")
def gain_node(state): return generate_plan(state, "Weight Gain")
def balanced_node(state): return generate_plan(state, "Balanced")

# STEP 8: Nutrition calculator
def nutrition_summary(state: dict) -> dict:
    bmr = 10 * state['weight'] + 6.25 * state['height'] - 5 * state['age']
    bmr += -161 if state['gender'] == 'female' else 5
    factor = {'low': 1.2, 'moderate': 1.55, 'high': 1.725}[state['activity_level']]
    calories = bmr * factor
    protein = state['weight'] * 1.2
    state.update({"calories": round(calories), "protein": round(protein)})
    print("\n📊 Daily Nutrition Goal:")
    print(f"Calories: {state['calories']} kcal, Protein: {state['protein']} g")
    return state

# STEP 9: Track meals
def track_meals(state: dict) -> dict:
    print("\n🧾 What did you eat today:")
    meals = {meal: input(f"🍽️ {meal.capitalize()}: ") for meal in ['breakfast', 'lunch', 'dinner', 'snacks']}
    meal_summary = "\n".join([f"{m.capitalize()}: {v}" for m, v in meals.items()])
    prompt = f"Estimate total calories and protein for:\n{meal_summary}\nFormat: Calories: X kcal, Protein: Y g"
    response = llm.invoke([HumanMessage(content=prompt)])
    state.update({"meal_summary": meal_summary, "meal_analysis": response.content.strip()})
    print("\n📋 Logged Intake:")
    print(response.content.strip())
    return state

# STEP 10: Remaining calories/protein
def track_remaining(state: dict) -> dict:
    cal = re.search(r'Calories\D+(\d+)', state["meal_analysis"])
    prot = re.search(r'Protein\D+(\d+)', state["meal_analysis"])
    cals = int(cal.group(1)) if cal else 0
    prots = int(prot.group(1)) if prot else 0
    rc, rp = max(state['calories'] - cals, 0), max(state['protein'] - prots, 0)
    print("\n📉 Remaining Today:")
    print(f"Calories left: {rc} kcal, Protein left: {rp} g")
    state.update({"remaining_calories": rc, "remaining_protein": rp})
    return state

# STEP 11: Suggest exercise
def suggest_exercise(state: dict) -> dict:
    prompt = f"Suggest a short Indian home workout (can include yoga) for Goal: {state['goal']}, Gender: {state['gender']}, Age: {state['age']}, Health: {state['health_issue']}"
    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n🏃 Exercise/Yoga:")
    print(response.content.strip())
    state["exercise"] = response.content.strip()
    return state

# STEP 12: Export as PDF
# STEP 12: Export as PDF with Google Colab download
from google.colab import files

def export_to_pdf(state: dict) -> dict:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"NutriAI Health Report for {state['name']}", ln=True, align='C')
    pdf.ln(10)

    # Remove emojis and non-ASCII characters before writing to PDF
    def clean_text(text): return re.sub(r'[^\x00-\x7F]+', '', text)

    user_info = f"""
    Name: {state['name']}
    Age: {state['age']}
    Gender: {state['gender']}
    Goal: {state['goal']}
    Diet: {state['preference']}
    Region: {state['region']}
    Health Issue: {state['health_issue']}
    Height: {state['height']} cm
    Weight: {state['weight']} kg
    Activity: {state['activity_level']}
    """
    pdf.multi_cell(0, 10, txt=clean_text(user_info))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Nutrition Summary", ln=True)
    pdf.set_font("Arial", size=12)
    nutrition_summary_text = f"Calories Needed: {state['calories']} kcal\nProtein Needed: {state['protein']} g"
    pdf.multi_cell(0, 10, txt=clean_text(nutrition_summary_text))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Diet Plan", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(state["plan"]))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Meal Log", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(state["meal_summary"]))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Nutritional Analysis", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(state["meal_analysis"]))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Remaining Calories/Protein", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(f"Calories left: {state['remaining_calories']} kcal\nProtein left: {state['remaining_protein']} g"))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Exercise Recommendation", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(state["exercise"]))

    output_path = "NutriAI_Report.pdf"  # Don't use /content/ prefix
    pdf.output(output_path)

    print("\n📥 PDF Report is ready. Triggering download...")
    files.download(output_path)
    state["pdf_path"] = output_path
    return state

# STEP 13: Build LangGraph flow
builder = StateGraph(dict)
builder.set_entry_point("get_user_input")
builder.add_node("get_user_input", get_user_input)
builder.add_node("classify", classify_goal)
builder.add_node("loss", loss_node)
builder.add_node("gain", gain_node)
builder.add_node("balanced", balanced_node)
builder.add_node("summary", nutrition_summary)
builder.add_node("track_meals", track_meals)
builder.add_node("track_remaining", track_remaining)
builder.add_node("exercise", suggest_exercise)
builder.add_node("export_pdf", export_to_pdf)

builder.add_edge("get_user_input", "classify")
builder.add_conditional_edges("classify", diet_router, {"loss": "loss", "gain": "gain", "balanced": "balanced"})
builder.add_edge("loss", "summary")
builder.add_edge("gain", "summary")
builder.add_edge("balanced", "summary")
builder.add_edge("summary", "track_meals")
builder.add_edge("track_meals", "track_remaining")
builder.add_edge("track_remaining", "exercise")
builder.add_edge("exercise", "export_pdf")
builder.add_edge("export_pdf", END)

# STEP 14: Run the AI agent
final_state = builder.compile().invoke({})
