import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- Load data ---
data = pd.read_csv("FoodCostDataset.csv")
data.fillna(data.mean(numeric_only=True), inplace=True)

# --- Train model ---
X = data[['Calories (kcal)', 'Carbohydrates (g)', 'Protein (g)',
          'Fats (g)', 'Free Sugar (g)', 'Fibre (g)', 'Sodium (mg)',
          'Calcium (mg)', 'Iron (mg)', 'Vitamin C (mg)', 'Folate (µg)']]
y = data['Estimated_Cost_per_100g(INR)']

model = LinearRegression()
model.fit(X, y)

# --- App UI ---
st.title("🍽️ AI-Powered Food Cost Optimizer")
st.write("Predict the estimated food cost (₹ per 100g) based on nutrient values.")

# Input fields
calories = st.number_input("Calories (kcal)", 0.0, 1000.0, 200.0)
carbs = st.number_input("Carbohydrates (g)", 0.0, 200.0, 30.0)
protein = st.number_input("Protein (g)", 0.0, 100.0, 10.0)
fats = st.number_input("Fats (g)", 0.0, 100.0, 5.0)
sugar = st.number_input("Free Sugar (g)", 0.0, 100.0, 2.0)
fiber = st.number_input("Fibre (g)", 0.0, 100.0, 3.0)
sodium = st.number_input("Sodium (mg)", 0.0, 5000.0, 150.0)
calcium = st.number_input("Calcium (mg)", 0.0, 1000.0, 50.0)
iron = st.number_input("Iron (mg)", 0.0, 50.0, 2.0)
vitc = st.number_input("Vitamin C (mg)", 0.0, 200.0, 10.0)
folate = st.number_input("Folate (µg)", 0.0, 1000.0, 100.0)

# Prediction button
if st.button("🔮 Predict Cost"):
    input_data = pd.DataFrame({
        'Calories (kcal)': [calories],
        'Carbohydrates (g)': [carbs],
        'Protein (g)': [protein],
        'Fats (g)': [fats],
        'Free Sugar (g)': [sugar],
        'Fibre (g)': [fiber],
        'Sodium (mg)': [sodium],
        'Calcium (mg)': [calcium],
        'Iron (mg)': [iron],
        'Vitamin C (mg)': [vitc],
        'Folate (µg)': [folate]
    })
    
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Estimated Cost per 100g: ₹{prediction:.2f}")
