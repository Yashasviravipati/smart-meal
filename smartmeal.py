import streamlit as st
import requests

# Hugging Face API information
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": "Bearer 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"}

# Function to get meal plan with descriptions from Hugging Face
def get_meal_plan_with_descriptions(calories, restrictions):
    # Structuring the prompt to provide clearer instructions to the model
    prompt = (
        f"Create a detailed meal plan for an entire day that provides approximately {calories} calories. "
        f"Include breakfast, lunch, dinner, and two snacks, with each meal having a brief description. "
        f"Consider the following dietary restrictions: {', '.join(restrictions)}. "
        f"Each meal should include the following details: meal name, main ingredients, and a short description. "
    )
    
    # Making the API request
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # Check response status and extract meal plan if successful
    if response.ok:
        try:
            meal_plan = response.json()[0].get("generated_text", "No meal plan generated.")
        except (KeyError, IndexError, TypeError):
            meal_plan = "Meal plan could not be generated due to unexpected response format."
    else:
        meal_plan = f"Meal plan could not be generated. Error: {response.status_code} - {response.text}"
    
    return meal_plan

# Calorie calculation function
def calculate_calories(age, weight, height, gender):
    # Using the Harris-Benedict equation for BMR and assuming moderate activity level
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    daily_calories = bmr * 1.55  # Moderate activity factor
    return daily_calories

# Streamlit application
st.title("Daily Calorie Intake & Meal Plan with Descriptions")

# Input fields
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, step=0.1)
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
gender = st.selectbox("Gender", ["Male", "Female"])
restrictions = st.multiselect("Dietary Restrictions", ["Diabetic", "Vegan", "Vegetarian", "Gluten-Free", "Lactose-Free", "Low-Carb"])

# Calculate button
if st.button("Calculate & Get Meal Plan"):
    if name and age and weight and height and gender:
        daily_calories = calculate_calories(age, weight, height, gender)
        meal_plan = get_meal_plan_with_descriptions(daily_calories, restrictions)
        st.success(f"Hello {name}! Your daily caloric requirement is approximately {daily_calories:.2f} calories.")
        st.subheader("Suggested Meal Plan with Descriptions:")
        st.write(meal_plan)
    else:
        st.error("Please fill in all fields.")
