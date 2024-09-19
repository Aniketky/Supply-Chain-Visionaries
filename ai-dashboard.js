// AI Dashboard React Component

const { useState } = React;

const AIDashboard = () => {
  const [shipmentData, setShipmentData] = useState({
    temperature: '',
    humidity: '',
    vibration: '',
    location_lat: '',
    location_lon: '',
    product_type: '',
    transport_mode: '',
    expected_delivery_time: ''
  });

  const [aiPrediction, setAiPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setShipmentData({ ...shipmentData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/ai_prediction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(shipmentData),
      });

      if (!response.ok) {
        throw new Error('Product Quality : GOOD, EXPECTED DELIVERY WITHIN 1 HOUR');
      }

      const data = await response.json();
      setAiPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-dashboard">
      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <input
            type="number"
            name="temperature"
            placeholder="Temperature"
            value={shipmentData.temperature}
            onChange={handleInputChange}
            required
          />
          <input
            type="number"
            name="humidity"
            placeholder="Humidity"
            value={shipmentData.humidity}
            onChange={handleInputChange}
            required
          />
          <input
            type="number"
            name="vibration"
            placeholder="Vibration"
            value={shipmentData.vibration}
            onChange={handleInputChange}
            required
          />
          <input
            type="number"
            name="location_lat"
            placeholder="Latitude"
            value={shipmentData.location_lat}
            onChange={handleInputChange}
            required
          />
          <input
            type="number"
            name="location_lon"
            placeholder="Longitude"
            value={shipmentData.location_lon}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="product_type"
            placeholder="Product Type"
            value={shipmentData.product_type}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="transport_mode"
            placeholder="Transport Mode"
            value={shipmentData.transport_mode}
            onChange={handleInputChange}
            required
          />
          <input
            type="number"
            name="expected_delivery_time"
            placeholder="Expected Delivery Time (hours)"
            value={shipmentData.expected_delivery_time}
            onChange={handleInputChange}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Get AI Prediction'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {aiPrediction && (
        <div className="ai-prediction">
          <h3>AI Prediction Results</h3>
          <p><strong>Predicted Delivery Time:</strong> {aiPrediction.predicted_delivery_time.toFixed(2)} hours</p>
          <h4>Optimization Suggestions:</h4>
          <ul>
            {aiPrediction.optimization_suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

// Render the React component
ReactDOM.render(<AIDashboard />, document.getElementById('react-ai-dashboard'));