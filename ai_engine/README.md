# AI Sustainability Advisor System

## Overview

This AI-powered sustainability advisor analyzes industrial data from Energy, Fuel, Air Quality, and Carbon Emission modules to provide intelligent recommendations, predictions, and scoring for environmental sustainability.

## Architecture

```
ai_engine/
├── agent.py          # Main AI agent with OpenAI integration
├── analyzer.py       # Data analysis and problem detection
├── recommender.py    # Smart recommendation generation
├── predictor.py      # ML models for predictions
├── scorer.py         # Sustainability scoring system
├── views.py          # API endpoints
├── urls.py           # URL routing
└── README.md         # This documentation
```

## Core Components

### 1. Data Analyzer (`analyzer.py`)
- Analyzes EnergyUsage, FuelConsumption, AirQuality, and CarbonEmission data
- Detects problems using configurable thresholds
- Provides insights for decision making

**Problem Detection Thresholds:**
- Energy: >1000 kWh average consumption
- Fuel: >10000 units total consumption
- Air Quality: AQI >150, CO2 >1000 ppm, PM2.5 >35 µg/m³

### 2. Recommender (`recommender.py`)
Generates targeted recommendations based on detected problems:

**Energy Recommendations:**
- Solar panel installation
- Smart energy monitoring
- Renewable energy adoption

**Fuel Recommendations:**
- Clean fuel transitions
- Efficiency optimization
- Emission reduction

**Air Quality Recommendations:**
- Filtration systems
- Ventilation improvements
- Emission controls

### 3. ML Predictor (`predictor.py`)
Machine learning models for future predictions:

**Algorithms Used:**
- Random Forest Regressor for energy and air quality
- Feature engineering with lag variables
- Time series analysis

**Predictions:**
- Energy consumption trends
- Fuel usage patterns
- AQI forecasts
- Carbon emission projections

### 4. Sustainability Scorer (`scorer.py`)
Comprehensive scoring system (0-100):

**Scoring Factors:**
- Energy Efficiency (30% weight)
- Fuel Consumption (25% weight)
- Air Quality (25% weight)
- Carbon Emissions (20% weight)

**Score Categories:**
- 80-100: Excellent
- 60-79: Good
- 40-59: Moderate
- Below 40: High Risk

### 5. AI Agent (`agent.py`)
Intelligent chatbot with contextual responses:

**Capabilities:**
- Natural language processing
- Data-aware responses
- Personalized recommendations
- OpenAI integration (optional)

## API Endpoints

### POST /api/ai-advisor/
AI chatbot for sustainability questions.

**Request:**
```json
{
  "question": "How can we reduce energy consumption?"
}
```

**Response:**
```json
{
  "question": "How can we reduce energy consumption?",
  "answer": "Your current sustainability score is 65/100 (Good). Based on your energy data showing average consumption of 1200 kWh, I recommend: - Install solar panels or wind turbines to reduce reliance on grid electricity - Implement smart energy monitoring systems to identify idle equipment"
}
```

### GET /api/ai/sustainability-score/
Get comprehensive sustainability score.

**Response:**
```json
{
  "overall_score": 72.5,
  "category": "Good",
  "color": "blue",
  "breakdown": {
    "energy": {"score": 75, "weight": 0.3},
    "fuel": {"score": 70, "weight": 0.25},
    "air_quality": {"score": 65, "weight": 0.25},
    "carbon": {"score": 80, "weight": 0.2}
  }
}
```

### GET /api/ai/predictions/
Get ML-based predictions.

**Response:**
```json
{
  "energy_predictions": [
    {"date": "2024-01-15", "prediction": 1150.5},
    {"date": "2024-01-16", "prediction": 1180.2}
  ],
  "aqi_predictions": [
    {"date": "2024-01-15", "aqi_prediction": 145.5},
    {"date": "2024-01-16", "aqi_prediction": 152.1}
  ]
}
```

## Machine Learning Models

### Training Data Requirements
- Minimum 30 days of historical data
- Consistent data collection
- No missing critical values

### Model Performance
- Energy Model: R² > 0.75 (typical)
- AQI Model: R² > 0.70 (typical)
- Automatic retraining on new data

### Feature Engineering
- Temporal features (day of year, month)
- Lag features (previous days' values)
- Categorical encoding for fuel types
- Rolling averages and trends

## OpenAI Integration

### Setup
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Enhanced Features
- Natural language understanding
- Contextual responses
- Advanced reasoning
- Personalized advice

### Fallback Mode
If OpenAI is unavailable, the system uses rule-based AI with:
- Keyword matching
- Template responses
- Data-driven recommendations

## Usage Examples

### Basic Queries
```
"How can we reduce pollution?"
"Why is our energy consumption high?"
"What does AQI 150 mean?"
```

### Advanced Queries
```
"Help me improve our sustainability score"
"Show me predictions for next month"
"What are our biggest environmental risks?"
```

### Data-Aware Responses
The AI analyzes your actual data to provide:
- Specific recommendations based on your metrics
- Personalized improvement plans
- Risk assessments
- Cost-benefit analysis

## Configuration

### Thresholds
Modify thresholds in `analyzer.py`:
```python
# Energy thresholds
ENERGY_HIGH_THRESHOLD = 1000  # kWh

# Air quality thresholds
AQI_POOR_THRESHOLD = 150
CO2_HIGH_THRESHOLD = 1000
PM25_HIGH_THRESHOLD = 35
```

### Scoring Weights
Adjust scoring weights in `scorer.py`:
```python
weights = {
    'energy': 0.3,
    'fuel': 0.25,
    'air_quality': 0.25,
    'carbon': 0.2
}
```

## Data Sources

### Required Data Models
- `EnergyUsage`: Consumption tracking
- `FuelConsumption`: Fuel usage and emissions
- `AirQuality`: Environmental monitoring
- `CarbonEmission`: GHG emissions

### Data Quality
- Consistent date formatting
- Complete records
- Realistic value ranges
- Regular updates

## Performance Optimization

### Caching
- Model predictions cached for 1 hour
- Score calculations cached for 30 minutes
- Database query optimization

### Scalability
- Asynchronous ML training
- Batch processing for large datasets
- Horizontal scaling support

## Monitoring & Maintenance

### Health Checks
- Model accuracy monitoring
- Data quality validation
- API response time tracking

### Retraining
- Automatic model retraining on new data
- Performance degradation detection
- Manual retraining triggers

## Security Considerations

### Data Access
- Role-based permissions
- Industry-specific data isolation
- Audit logging

### API Security
- JWT authentication
- Rate limiting
- Input validation

## Future Enhancements

### Advanced Features
- Real-time anomaly detection
- Predictive maintenance alerts
- Carbon credit optimization
- Regulatory compliance checking

### Integration Options
- IoT sensor data
- Weather API integration
- Energy market data
- Regulatory database

## Troubleshooting

### Common Issues
1. **Low prediction accuracy**: Check data quality and quantity
2. **Slow responses**: Enable caching and optimize queries
3. **OpenAI errors**: Verify API key and fallback to rule-based mode

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Code Standards
- Type hints for all functions
- Comprehensive docstrings
- Unit tests for all components
- PEP 8 compliance

### Testing
```bash
# Run ML model tests
python -m pytest ai_engine/tests/test_predictor.py

# Run API tests
python -m pytest ai_engine/tests/test_views.py
```

This AI system transforms raw industrial data into actionable sustainability insights, helping facilities reduce environmental impact and improve operational efficiency.