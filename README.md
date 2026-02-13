# Heart Failure Prediction Dashboard

A modern, professional web application built with Streamlit for predicting heart disease risk using Machine Learning.

## ✨ Features

- **🎨 Glassmorphism UI Design**: Beautiful dark-themed interface with modern glass effects
- **📊 Interactive Visualizations**: Dynamic gauge charts and probability displays using Plotly
- **🔍 Real-time Predictions**: Instant heart disease risk assessment using Random Forest ML model
- **✅ Input Validation**: Comprehensive validation to ensure realistic medical values
- **📱 Responsive Design**: Works seamlessly across desktop and mobile devices
- **🎯 Feature Importance**: Visual display of key risk factors affecting predictions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the files**
   ```bash
   # Navigate to the project directory
   cd heart-failure-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   - The app will automatically open in your default browser
   - Default URL: `http://localhost:8501`

## 📦 Project Structure

```
heart-failure-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## 🎯 How to Use

### 1. Enter Patient Information

Fill in the following details in the sidebar:

**Demographics:**
- Age (1-120 years)
- Sex (Male/Female)

**Clinical Measurements:**
- Chest Pain Type (4 options)
- Resting Blood Pressure (50-250 mm Hg)
- Cholesterol (0-600 mg/dL)
- Fasting Blood Sugar (Yes/No)

**ECG & Exercise Data:**
- Resting ECG (3 options)
- Maximum Heart Rate (60-220 bpm)
- Exercise-Induced Angina (Yes/No)
- ST Depression/Oldpeak (-5.0 to 10.0)
- ST Slope (3 options)

### 2. Get Predictions

Click the **"🔍 Predict Risk"** button to:
- View diagnosis (At Risk / Healthy)
- See confidence percentage
- Assess risk level (High/Medium/Low)
- Visualize probabilities with interactive gauges
- Review key risk factors

### 3. Review Recommendations

The dashboard provides personalized recommendations based on the prediction results.

## 🔧 Customization

### Using Your Own Model

Replace the sample data generation in `load_and_train_model()` with your actual dataset:

```python
# Load your CSV file
df = pd.read_csv('your_heart_data.csv')

# Encode categorical features
encoder = OrdinalEncoder()
categorical = ['Sex','ChestPainType','RestingECG', 'ExerciseAngina','ST_Slope']
df[categorical] = encoder.fit_transform(df[categorical])

# Continue with model training...
```

### Styling

All CSS styles are contained in the `load_custom_css()` function. Modify colors, gradients, and effects to match your brand:

```python
# Change gradient colors
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

# Adjust glass effect opacity
background: rgba(255, 255, 255, 0.08);
```

## 🌐 Deployment Options

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click

### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t heart-failure-app .
   docker run -p 8501:8501 heart-failure-app
   ```

## 📊 Model Information

- **Algorithm**: Random Forest Classifier
- **Parameters**:
  - n_estimators: 100
  - max_depth: 6
  - min_samples_leaf: 3
- **Features**: 11 cardiovascular health indicators
- **Output**: Binary classification (Heart Disease: Yes/No)

## 🛡️ Input Validation Ranges

| Feature | Min | Max | Unit |
|---------|-----|-----|------|
| Age | 1 | 120 | years |
| Resting BP | 50 | 250 | mm Hg |
| Cholesterol | 0 | 600 | mg/dL |
| Max Heart Rate | 60 | 220 | bpm |
| Oldpeak | -5.0 | 10.0 | - |

## ⚠️ Important Disclaimer

This application is for educational and demonstration purposes only. The predictions should **NOT** be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source
---

**Built using Streamlit, scikit-learn, and Plotly**
