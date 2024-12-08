import streamlit as st
import requests

# Hugging Face API information
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": "Bearer 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"}

# Function to get meal plan with descriptions from Hugging Face
def get_meal_plan_with_descriptions(calories, restrictions):
    # Structuring the prompt to provide clearer instructions to the model
    prompt = (
        f"Design a detailed meal plan for one day, tailored to provide approximately {calories} calories. "
        f"The plan should include five meals: breakfast, lunch, dinner, and two snacks. For each meal, specify: "
        f"The meal name, the main ingredient, and a brief description of the meal. "
        f"Ensure the meal plan adheres to the following dietary restrictions: {', '.join(restrictions)}. "
        f"The total calorie count should align with the specified target, and the meals should be diverse and balanced."
    )
    
    # Hugging Face API request payload
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,  # Adjust for balance between determinism and creativity
            "max_new_tokens": 500,  # Ensure sufficient space for detailed meal plan
            "return_full_text": False  # Return only the generated text
        },
        "options": {"use_cache": False}  # Optional: Disable caching to ensure a fresh response
    }
    
    # Making the API request
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check response status and extract meal plan if successful
    if response.ok:
        try:
            meal_plan = response.json()[0].get("generated_text", "No meal plan generated.")
        except (KeyError, IndexError, TypeError):
            meal_plan = "Meal plan could not be generated due to unexpected response format."
    else:
        meal_plan = f"Meal plan could not be generated. Error: {response.status_code} - {response.text}"
    
    return meal_plan
