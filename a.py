import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import datetime

# Define the initial data
data = {
    "Temperature": [25, 30, 22, 28, 26, 24, 27, 29, 23, 25],
    "Humidity": [60, 65, 70, 58, 62, 68, 64, 66, 72, 69],
    "Vibration": [2.5, 3.2, 2.8, 3.5, 2.9, 3.1, 2.7, 3.0, 2.6, 3.3],
    "Latitude": [34.0522, 40.7128, 37.7749, 41.8781, 34.0522, 40.7128, 37.7749, 41.8781, 34.0522, 40.7128],
    "Longitude": [-118.2437, -74.0060, -122.4194, -87.6298, -118.2437, -74.0060, -122.4194, -87.6298, -118.2437, -74.0060],
    "Product Type": ["Food", "Electronics", "Pharmaceuticals", "Food", "Electronics", "Pharmaceuticals", "Food", "Electronics", "Pharmaceuticals", "Food"],
    "Transport Mode": ["Truck", "Ship", "Airplane", "Truck", "Ship", "Airplane", "Truck", "Ship", "Airplane", "Truck"],
    "Shipment Status": ["Delivered", "Delayed", "Delivered", "Delivered", "Delayed", "Delivered", "Delivered", "Delayed", "Delivered", "Delivered"]
}

df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=["Product Type", "Transport Mode"])

X = df.drop("Shipment Status", axis=1)
y = df["Shipment Status"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

def check_product_status(product_type, temperature, humidity, vibration, transport_mode, days_in_transit):
    if product_type == "Food":
        if temperature > 30 or humidity > 70 or vibration > 3.5 or days_in_transit > 5:
            return "Spoiled"
    elif product_type == "Electronics":
        if humidity > 80 or vibration > 4.0:
            return "Damaged"
    elif product_type == "Pharmaceuticals":
        if temperature < 2 or temperature > 30 or days_in_transit > 7:
            return "Expired"
    
    return "Good"

# Get user input
temperature = float(input("Enter temperature: "))
humidity = float(input("Enter humidity: "))
vibration = float(input("Enter vibration: "))
latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))
product_type = input("Enter product type (Food/Electronics/Pharmaceuticals): ")
transport_mode = input("Enter transport mode (Truck/Ship/Airplane): ")
days_in_transit = int(input("Enter number of days in transit: "))

# Prepare input data for prediction
input_data = pd.DataFrame({
    "Temperature": [temperature],
    "Humidity": [humidity],
    "Vibration": [vibration],
    "Latitude": [latitude],
    "Longitude": [longitude],
    "Product Type_Electronics": [1 if product_type == "Electronics" else 0],
    "Product Type_Food": [1 if product_type == "Food" else 0],
    "Product Type_Pharmaceuticals": [1 if product_type == "Pharmaceuticals" else 0],
    "Transport Mode_Airplane": [1 if transport_mode == "Airplane" else 0],
    "Transport Mode_Ship": [1 if transport_mode == "Ship" else 0],
    "Transport Mode_Truck": [1 if transport_mode == "Truck" else 0]
})

# Make prediction
prediction = model.predict(input_data)[0]
print("Shipment Status Prediction:", prediction)

# Check product status
product_status = check_product_status(product_type, temperature, humidity, vibration, transport_mode, days_in_transit)
print("Product Status:", product_status)

# Calculate model accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
