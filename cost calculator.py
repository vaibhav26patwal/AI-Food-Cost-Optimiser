import pandas as pd

data = pd.read_csv("FoodCostDataset.csv")
print(data.columns)

data.columns = data.columns.str.strip()

def find_alternatives(dish_name):
    print(f"\n🔎 Searching for alternatives to '{dish_name}'...\n")
    # Find the dish
    dish = data[data["Dish Name"].str.lower().str.contains(dish_name.lower(), na=False)]
    
    if dish.empty:
        print("❌ Dish not found. Try a different name.")
        return
    
    dish_info = dish.iloc[0]
    category = dish_info["Category"]
    cost = dish_info["Estimated_Cost_per_100g(INR)"]
    calories = dish_info["Calories (kcal)"]
    
    print(f"🍽️ {dish_info['Dish Name']}  |  Category: {category}  |  Cost: ₹{cost:.2f}/100g")
    
    # Find cheaper similar dishes in same category
    candidates = data[(data["Category"] == category) &
                      (data["Estimated_Cost_per_100g(INR)"] < cost)]
    
    if candidates.empty:
        print("\n✅ This is already one of the cheapest dishes in its category.")
        return
    
    # Sort by how close the calories are
    candidates["CalorieDiff"] = abs(candidates["Calories (kcal)"] - calories)
    best_alts = candidates.sort_values(["CalorieDiff", "Estimated_Cost_per_100g(INR)"]).head(3)
    
    print("\n💡 Top 3 Cheaper Alternatives:")
    for _, alt in best_alts.iterrows():
        saving = ((cost - alt["Estimated_Cost_per_100g(INR)"]) / cost) * 100
        print(f"➡️ {alt['Dish Name']}  |  ₹{alt['Estimated_Cost_per_100g(INR)']:.2f}/100g  |  "
              f"Calories: {alt['Calories (kcal)']:.1f}  |  💰 Save {saving:.1f}%")

dish_name = input("Enter a dish name: ")
find_alternatives(dish_name)
# Machine Learning Model to Predict Cost Based on Nutrients
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

data = pd.read_csv("FoodCostDataset.csv")

data.fillna(data.mean(numeric_only=True), inplace=True)

X = data[['Calories (kcal)', 'Carbohydrates (g)', 'Protein (g)', 
          'Fats (g)', 'Free Sugar (g)', 'Fibre (g)', 'Sodium (mg)', 
          'Calcium (mg)', 'Iron (mg)', 'Vitamin C (mg)', 'Folate (µg)']]

y = data['Estimated_Cost_per_100g(INR)']

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Evaluate
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R² Score: {r2_score(y_test, y_pred):.2f}")

# Example prediction
sample_data = pd.DataFrame({
    'Calories (kcal)': [200],
    'Carbohydrates (g)': [30],
    'Protein (g)': [10],
    'Fats (g)': [5],
    'Free Sugar (g)': [2],
    'Fibre (g)': [3],
    'Sodium (mg)': [150],
    'Calcium (mg)': [50],
    'Iron (mg)': [2],
    'Vitamin C (mg)': [10],
    'Folate (µg)': [100]
})

predicted_cost = model.predict(sample_data)[0]
print(f"\n💰 Predicted Cost per 100g: ₹{predicted_cost:.2f}")
