import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI-Powered Food Nutrition Finder", layout="wide")

st.title("🍱 AI-Powered Food Nutrition Finder")
st.write("Type a food item to get its nutritional details instantly!")

st.caption("💡 Demo Mode: Cost predictions are simulated and not real-world prices.")

# --- Search Bar ---
food_item = st.text_input("🔍 What do you want to eat?", placeholder="e.g. Paneer Butter Masala, Chicken Curry, Banana")

if food_item:
    # Fetch data from FoodData Central API
    api_key = "DEMO_KEY"  # Replace with your own API key (from https://fdc.nal.usda.gov/)
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_item}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["foods"]:
            food_data = data["foods"][0]  # take first result
            st.subheader(f"🍽️ {food_data['description']}")
            
            nutrients = {n['nutrientName']: n['value'] for n in food_data['foodNutrients']}
            df = pd.DataFrame(list(nutrients.items()), columns=["Nutrient", "Value"])
            st.dataframe(df)
            
            # Optional: Calculate estimated cost (simple model)
            calories = nutrients.get("Energy", 0)
            protein = nutrients.get("Protein", 0)
            fats = nutrients.get("Total lipid (fat)", 0)
            predicted_cost = round(5 + (0.02 * calories) + (0.2 * protein) + (0.1 * fats), 2)
            
            st.success(f"💰 Estimated Food Cost: ₹{predicted_cost} per 100g")
        else:
            st.warning("No data found for this food.")
    else:
        st.error("API request failed. Please try again later.")

