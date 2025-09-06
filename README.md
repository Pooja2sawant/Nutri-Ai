# 🌟 **NutriAI – Your AI-Powered Indian Diet Assistant** 🌟

**NutriAI** is a friendly AI diet assistant that generates **personalized Indian meal plans**, tracks calories & protein intake, and suggests **home exercises & yoga** based on your **health goals, diet preferences, region, age, gender, and activity level**.
Built using **Google Gemini API (Gemini 1.5 Flash)**, **LangGraph**, and **LangChain**, NutriAI also lets you log meals and export a **complete PDF health report**. Perfect for **weight loss 🏋️, weight gain 💪, or balanced diet 🥗** planning with traditional Indian cuisine.


## 🍽️ **Features**

* ✅ Personalized Indian meal plans based on:

  * 👤 Age, Gender, Height, Weight
  * 🎯 Health goals (weight loss, weight gain, balanced diet)
  * 🌿 Diet preference (veg, non-veg, vegan)
  * 🍛 Indian cuisine region
  * 🩺 Health issues (PCOS, acne, thyroid, etc.)
  * 🏃 Activity level (low, moderate, high)
* 🔥 Daily calorie and protein calculation
* 🧾 Meal logging with AI-based nutritional analysis
* 📉 Track remaining calories & protein for the day
* 🧘‍♂️ Suggests short home exercises or yoga routines
* 📥 Export **PDF health report** with full details

---

## 🛠️ **Installation**

1. Clone the repository:

```bash
git clone https://github.com/Pooja2sawant/Nutri-AI.git
cd NutriAI
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the main script (recommended in **Google Colab** for easy API key input & PDF download):

```bash
python Nutri_Ai.py
```

4. Enter your **Google Gemini API key 🔑** securely when prompted.

---

## 🚀 **Usage**

1. Run the AI agent script.
2. Enter your personal details:

   * 👤 Name
   * 🎂 Age
   * ⚧ Gender
   * 📏 Height & ⚖️ Weight
   * 🎯 Health goal
   * 🌿 Diet preference & 🍛 Region
   * 🩺 Health issues & 🏃 Activity level
3. NutriAI will:

   * 🍽️ Generate a personalized Indian meal plan
   * 📊 Calculate your daily nutrition needs
   * 🧾 Track meals & estimate calories/protein
   * 📉 Show remaining calories & protein
   * 🧘 Suggest exercises or yoga routines
   * 📥 Export a downloadable **PDF health report**

---

## 🧰 **Technologies Used**

* **Python 3.10+ 🐍**
* **Google Gemini API (Gemini 1.5 Flash) 🤖**
* **LangGraph** – AI workflow management
* **LangChain & langchain-google-genai** – LLM integration
* **Matplotlib 📊** – Optional data visualization
* **FPDF 📄** – PDF generation
* **Google Colab ☁️** – Seamless deployment

---

## 📂 **Project Structure**

```
NutriAI/
│
├── nutri_ai.py        # Main AI agent script
├── requirements.txt   # Dependencies
└── README.md          # Project description
```

## ⚠️ **Notes**

* Recommended to use **Google Colab** for secure API key input & PDF download.
* NutriAI focuses on **Indian diets & regional cuisines**.
* All outputs are **AI-based recommendations**. Consult a certified dietitian for medical/clinical advice.

---

## 📝 **License**

MIT License © 2025 Pooja Sawant
