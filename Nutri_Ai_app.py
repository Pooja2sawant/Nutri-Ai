import streamlit as st
import numpy as np
import pandas as pd
from fpdf import FPDF
from langgraph import Graph
from langchain import OpenAI
from langchain_google_genai import GoogleGenAI
import getpass
import datetime
import json

# -------------------------------
# Streamlit App Start
# -------------------------------

st.title("NutriAI - Your AI Diet Assistant")

# Welcome message
st.write("Namaste! I am NutriAI, your Indian dietician.")

# User info
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=120)
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])

# Health goal
goal = st.selectbox(
    "What is your goal?",
    ["Weight Loss", "Weight Gain", "Maintain Weight", "Healthy Diet"]
)

# Diet preference
diet_pref = st.selectbox(
    "Diet Preference:",
    ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian"]
)

# Meals input
st.subheader("Meals Today")
breakfast = st.text_input("Breakfast:")
lunch = st.text_input("Lunch:")
dinner = st.text_input("Dinner:")
snacks = st.text_input("Snacks:")

# Optional: User clicks to generate diet plan
if st.button("Generate Diet Plan"):
    st.write(f"Generating diet plan for {name}, Age: {age}, Goal: {goal}, Diet: {diet_pref}...")
    
    # Example: placeholder for AI-generated plan
    st.success("Your personalized diet plan will appear here!")

# Optional: Export to PDF
if st.button("Download Diet Plan as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"NutriAI Diet Plan for {name}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Age: {age}, Gender: {gender}", ln=True)
    pdf.cell(200, 10, txt=f"Goal: {goal}", ln=True)
    pdf.cell(200, 10, txt=f"Diet Preference: {diet_pref}", ln=True)
    pdf.cell(200, 10, txt="Meals:", ln=True)
    pdf.cell(200, 10, txt=f"Breakfast: {breakfast}", ln=True)
    pdf.cell(200, 10, txt=f"Lunch: {lunch}", ln=True)
    pdf.cell(200, 10, txt=f"Dinner: {dinner}", ln=True)
    pdf.cell(200, 10, txt=f"Snacks: {snacks}", ln=True)
    
    pdf.output("NutriAI_DietPlan.pdf")
    st.success("PDF generated successfully! Check your app folder for NutriAI_DietPlan.pdf")
