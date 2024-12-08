import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API client
API_KEY = os.getenv("AIzaSyClGQusntsKRRi5pDyQzjoBxzPafOCqlko")
genai.configure(api_key=API_KEY)

# Function to get meal plan with descriptions from Gemini
def get_meal_plan_with_descriptions(calories, restrictions):
    prompt = (
        f"Design a detailed meal plan for one day, tailored to provide approximately {calories} calories. "
        f"The plan should include five meals: breakfast, lunch, dinner, and two snacks. For each meal, specify: "
        f"The meal name, the main ingredient, and a brief description of the meal. "
        f"Ensure the meal plan adheres to the following dietary restrictions: {', '.join(restrictions)}. "
        f"The total calorie count should align with the specified target, and the meals should be diverse and balanced."
    )
    
    try:
        model = genai.GenerativeModel(model="gemini-1.5-flash")
        response = model.generate_content(prompt)
        meal_plan = response.text
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
