from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
from a import check_product_status

app = Flask(__name__)

# Load the model
with open('my_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    # Render the HTML page (frontend form)
    return render_template('index.html')

@app.route('/api/ai_prediction', methods=['POST'])
def predict():
    try:
        # Get data from the request (sent by AJAX from the frontend)
        data = request.get_json()

        # Create a DataFrame from the input data
        input_df = pd.DataFrame([data])

        # Preprocess the input data - one-hot encode categorical features
        input_df = pd.get_dummies(input_df, columns=["Product Type", "Transport Mode"])

        # Ensure the input DataFrame has all the columns the model expects
        expected_columns = ['Temperature', 'Humidity', 'Vibration', 'Latitude', 'Longitude', 
                            'Product Type_Electronics', 'Product Type_Food', 'Product Type_Pharmaceuticals', 
                            'Transport Mode_Airplane', 'Transport Mode_Ship', 'Transport Mode_Truck']
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0 

        # Make predictions
        prediction = model.predict(input_df)[0]
        shipment_status_prediction = prediction 

        # Check product status using the logic from a.py
        product_status = check_product_status(
            data['Product Type'], 
            data['Temperature'], 
            data['Humidity'], 
            data['Vibration'], 
            data['Transport Mode'], 
            data['days_in_transit']
        )

        # Prepare the response
        response = {
            'shipment_status_prediction': shipment_status_prediction,
            'product_status': product_status 
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
