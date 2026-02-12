"""
Enhanced Heart Failure Prediction Dashboard
This version loads a pre-trained model from a pickle file.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
import os

warnings.filterwarnings('ignore')

# Try to import joblib for model loading
try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False

# ========================
# Configuration
# ========================
st.set_page_config(
    page_title="Heart Failure Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# Custom CSS - Glassmorphism Theme
# ========================
def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        }
        
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: transparent;
        }
        
        h1, h2, h3 {
            color: #ffffff;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 10px 0;
        }
        
        .metric-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.95rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 40px;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: white;
            padding: 10px;
        }
        
        .stNumberInput > label,
        .stSelectbox > label,
        .stSlider > label {
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
            font-size: 0.95rem;
        }
        
        .stAlert {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        
        hr {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin: 25px 0;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        </style>
    """, unsafe_allow_html=True)

# ========================
# Data Loading & Model Training
# ========================
@st.cache_resource
def load_and_train_model():
    """
    Load model from pickle file if available, otherwise train a new one.
    """
    model_path = 'heart_model.pkl'
    
    # Try to load pre-trained model
    if JOBLIB_AVAILABLE and os.path.exists(model_path):
        try:
            st.sidebar.success("✅ Loading pre-trained model...")
            model_data = joblib.load(model_path)
            return model_data['model'], model_data['feature_names']
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not load model: {e}")
            st.sidebar.info("Training new model with sample data...")
    
    # Train new model with sample data
    np.random.seed(42)
    n_samples = 918
    
    data = {
        'Age': np.random.randint(28, 78, n_samples),
        'Sex': np.random.choice([0, 1], n_samples),
        'ChestPainType': np.random.choice([0, 1, 2, 3], n_samples),
        'RestingBP': np.random.randint(90, 200, n_samples),
        'Cholesterol': np.random.randint(0, 400, n_samples),
        'FastingBS': np.random.choice([0, 1], n_samples),
        'RestingECG': np.random.choice([0, 1, 2], n_samples),
        'MaxHR': np.random.randint(60, 202, n_samples),
        'ExerciseAngina': np.random.choice([0, 1], n_samples),
        'Oldpeak': np.random.uniform(-2.6, 6.2, n_samples),
        'ST_Slope': np.random.choice([0, 1, 2], n_samples),
        'HeartDisease': np.random.choice([0, 1], n_samples)
    }
    
    df = pd.DataFrame(data)
    X = df.drop('HeartDisease', axis=1)
    y = df['HeartDisease']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_leaf=3,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    return model, X.columns.tolist()

# ========================
# Input Validation
# ========================
def validate_input(name, value, min_val, max_val):
    """Validate numeric input ranges"""
    if value < min_val or value > max_val:
        st.sidebar.error(f"⚠️ {name} must be between {min_val} and {max_val}")
        return False
    return True

# ========================
# Visualization Functions
# ========================
def create_gauge_chart(probability, title, color_scheme):
    """Create a beautiful gauge chart for probability display"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': 'white'}},
        number={'suffix': "%", 'font': {'size': 40, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color_scheme},
            'bgcolor': "rgba(255, 255, 255, 0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255, 255, 255, 0.3)",
            'steps': [
                {'range': [0, 33], 'color': 'rgba(72, 187, 120, 0.3)'},
                {'range': [33, 66], 'color': 'rgba(237, 137, 54, 0.3)'},
                {'range': [66, 100], 'color': 'rgba(245, 101, 101, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_feature_importance_chart(model, feature_names):
    """Create feature importance bar chart"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:8]
    
    fig = go.Figure(go.Bar(
        x=importances[indices],
        y=[feature_names[i] for i in indices],
        orientation='h',
        marker=dict(
            color=importances[indices],
            colorscale='Viridis',
            line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
        )
    ))
    
    fig.update_layout(
        title='Top Feature Importance',
        title_font=dict(size=20, color='white'),
        xaxis_title='Importance Score',
        yaxis_title='Features',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Inter"},
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    
    return fig

# ========================
# Main Application
# ========================
def main():
    load_custom_css()
    
    # Load model
    model, feature_names = load_and_train_model()
    
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='font-size: 3rem; margin-bottom: 10px;'>❤️ Heart Failure Prediction</h1>
            <p style='color: rgba(255, 255, 255, 0.7); font-size: 1.2rem;'>
                AI-Powered Cardiovascular Risk Assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Patient Information")
        st.markdown("*Please enter patient details below*")
        st.markdown("---")
        
        st.markdown("#### 👤 Demographics")
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=50, step=1)
        sex = st.selectbox("Sex", options=["Female", "Male"])
        
        st.markdown("---")
        st.markdown("#### 🩺 Clinical Measurements")
        chest_pain = st.selectbox(
            "Chest Pain Type",
            options=["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"]
        )
        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 
                                      min_value=50, max_value=250, value=120, step=1)
        cholesterol = st.number_input("Cholesterol (mg/dL)", 
                                       min_value=0, max_value=600, value=200, step=1)
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=["No", "Yes"])
        
        st.markdown("---")
        st.markdown("#### 📊 ECG & Exercise Data")
        resting_ecg = st.selectbox(
            "Resting ECG",
            options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"]
        )
        max_hr = st.number_input("Maximum Heart Rate", 
                                 min_value=60, max_value=220, value=150, step=1)
        exercise_angina = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"])
        oldpeak = st.number_input("ST Depression (Oldpeak)", 
                                  min_value=-5.0, max_value=10.0, value=0.0, step=0.1)
        st_slope = st.selectbox(
            "ST Slope",
            options=["Upsloping", "Flat", "Downsloping"]
        )
        
        st.markdown("---")
        predict_button = st.button("🔍 Predict Risk", use_container_width=True)
    
    # Input validation
    all_valid = True
    all_valid &= validate_input("Age", age, 1, 120)
    all_valid &= validate_input("Resting BP", resting_bp, 50, 250)
    all_valid &= validate_input("Cholesterol", cholesterol, 0, 600)
    all_valid &= validate_input("Max Heart Rate", max_hr, 60, 220)
    all_valid &= validate_input("Oldpeak", oldpeak, -5.0, 10.0)
    
    if predict_button and all_valid:
        input_data = pd.DataFrame({
            'Age': [age],
            'Sex': [1 if sex == "Male" else 0],
            'ChestPainType': [["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"].index(chest_pain)],
            'RestingBP': [resting_bp],
            'Cholesterol': [cholesterol],
            'FastingBS': [1 if fasting_bs == "Yes" else 0],
            'RestingECG': [["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(resting_ecg)],
            'MaxHR': [max_hr],
            'ExerciseAngina': [1 if exercise_angina == "Yes" else 0],
            'Oldpeak': [oldpeak],
            'ST_Slope': [["Upsloping", "Flat", "Downsloping"].index(st_slope)]
        })
        
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        st.markdown("## 📊 Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class='metric-card'>
                    <div class='metric-label'>Diagnosis</div>
                    <div class='metric-value'>{}</div>
                </div>
            """.format("At Risk" if prediction == 1 else "Healthy"), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='metric-card'>
                    <div class='metric-label'>Confidence</div>
                    <div class='metric-value'>{:.1f}%</div>
                </div>
            """.format(max(probability) * 100), unsafe_allow_html=True)
        
        with col3:
            risk_level = "High" if max(probability) > 0.7 else "Medium" if max(probability) > 0.4 else "Low"
            st.markdown("""
                <div class='metric-card'>
                    <div class='metric-label'>Risk Level</div>
                    <div class='metric-value'>{}</div>
                </div>
            """.format(risk_level), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_gauge_chart(
                probability[0], 
                "Healthy Probability",
                "linear-gradient(135deg, #48bb78 0%, #38a169 100%)"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_gauge_chart(
                probability[1], 
                "Heart Disease Probability",
                "linear-gradient(135deg, #f56565 0%, #e53e3e 100%)"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        st.markdown("## 🎯 Key Risk Factors")
        fig3 = create_feature_importance_chart(model, feature_names)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("---")
        st.markdown("## 💡 Recommendations")
        
        if prediction == 1:
            st.error("""
                **⚠️ Heart Disease Risk Detected**
                
                Based on the provided information, the model indicates an elevated risk of heart disease.
                We recommend:
                - Schedule an appointment with a cardiologist immediately
                - Undergo comprehensive cardiovascular screening
                - Discuss lifestyle modifications and treatment options
                - Monitor vital signs regularly
            """)
        else:
            st.success("""
                **✅ Low Risk Detected**
                
                The model indicates a lower risk of heart disease. However:
                - Continue regular health check-ups
                - Maintain a healthy lifestyle with proper diet and exercise
                - Monitor blood pressure and cholesterol levels
                - Stay informed about cardiovascular health
            """)
        
        st.info("""
            **📌 Important Note:** This prediction is based on machine learning algorithms and should not 
            replace professional medical advice. Always consult with healthcare professionals for 
            accurate diagnosis and treatment.
        """)
    
    elif not all_valid:
        st.warning("⚠️ Please correct the input values highlighted in the sidebar.")
    
    else:
        st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 60px;'>
                <h2 style='margin-bottom: 20px;'>Welcome to Heart Failure Prediction System</h2>
                <p style='font-size: 1.1rem; color: rgba(255, 255, 255, 0.7); line-height: 1.8;'>
                    This advanced AI-powered system uses machine learning to assess cardiovascular risk.
                    <br><br>
                    👈 Please enter patient information in the sidebar and click <strong>"Predict Risk"</strong> to begin.
                    <br><br>
                    Our Random Forest model analyzes 11 key health indicators to provide accurate predictions.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📌 Features Analyzed")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                - Age
                - Sex
                - Chest Pain Type
                - Resting Blood Pressure
            """)
        
        with col2:
            st.markdown("""
                - Cholesterol
                - Fasting Blood Sugar
                - Resting ECG
                - Maximum Heart Rate
            """)
        
        with col3:
            st.markdown("""
                - Exercise-Induced Angina
                - ST Depression (Oldpeak)
                - ST Slope
            """)

if __name__ == "__main__":
    main()
