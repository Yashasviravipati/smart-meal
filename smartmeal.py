import os
import streamlit as st
import requests

# Configure the Gemini API key
API_KEY = os.getenv("AIzaSyClGQusntsKRRi5pDyQzjoBxzPafOCqlko")
API_URL = f"https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5:generateText?key={API_KEY}"

# Function to get meal plan with descriptions using Gemini API
def get_meal_plan_with_descriptions(calories, restrictions):
    prompt = (
        f"Design a detailed meal plan for one day, tailored to provide approximately {calories:.2f} calories. "
        f"The plan should include five meals: breakfast, lunch, dinner, and two snacks. For each meal, specify:\n"
        f"- The meal name.\n"
        f"- The main ingredients.\n"
        f"- A brief description of the meal.\n"
        f"Ensure the meal plan adheres to the following dietary restrictions: {', '.join(restrictions)}.\n"
        f"The total calorie count should align with the specified target, and the meals should be diverse and balanced."
    )

    payload = {
        "prompt": {"text": prompt},
        "temperature": 0.7,  # Adjust creativity
        "maxOutputTokens": 700,  # Ensure detailed response
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        # Make the API request
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.ok:
            result = response.json()
            meal_plan = result["candidates"][0]["output"]
        else:
            meal_plan = f"Error generating meal plan: {response.status_code} - {response.text}"
    except Exception as e:
        meal_plan = f"Error generating meal plan: {str(e)}"
    
    return meal_plan

# Calorie calculation function
def calculate_calories(age, weight, height, gender):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    daily_calories = bmr * 1.55  # Moderate activity factor
    return daily_calories

# Streamlit application
st.title("Daily Calorie Intake & Meal Plan with Descriptions")

name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, step=0.1)
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
gender = st.selectbox("Gender", ["Male", "Female"])
restrictions = st.multiselect("Dietary Restrictions", ["Diabetic", "Vegan", "Vegetarian", "Gluten-Free", "Lactose-Free", "Low-Carb"])

if st.button("Calculate & Get Meal Plan"):
    if all([name, age, weight, height, gender]):
        daily_calories = calculate_calories(age, weight, height, gender)
        meal_plan = get_meal_plan_with_descriptions(daily_calories, restrictions)
        st.success(f"Hello {name}! Your daily caloric requirement is approximately {daily_calories:.2f} calories.")
        st.subheader("Suggested Meal Plan with Descriptions:")
        st.write(meal_plan)
    else:
        st.error("Please fill in all fields.")
