"""
Model Integration Helper
This script helps you integrate your trained model from the Jupyter notebook.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_and_save_model(csv_path='heart.csv', model_output='heart_model.pkl'):
    """
    Train the Random Forest model using your actual dataset and save it.
    
    Parameters:
    -----------
    csv_path : str
        Path to your heart.csv file
    model_output : str
        Path where the trained model will be saved
    
    Returns:
    --------
    model : RandomForestClassifier
        Trained model
    feature_names : list
        List of feature names
    """
    
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Encode categorical features
    print("\nEncoding categorical features...")
    encoder = OrdinalEncoder()
    categorical = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    df[categorical] = encoder.fit_transform(df[categorical])
    df = df.dropna()
    
    # Split features and target
    X = df.drop('HeartDisease', axis=1)
    y = df['HeartDisease']
    
    feature_names = X.columns.tolist()
    
    # Train-test split
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_leaf=3,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\nModel Performance:")
    print(f"Training Accuracy: {train_score:.4f}")
    print(f"Testing Accuracy: {test_score:.4f}")
    
    # Save model
    print(f"\nSaving model to {model_output}...")
    model_data = {
        'model': model,
        'feature_names': feature_names,
        'encoder': encoder
    }
    joblib.dump(model_data, model_output)
    
    print("✅ Model saved successfully!")
    print(f"\nTo use this model in the app, update the load_and_train_model() function:")
    print(f"model_data = joblib.load('{model_output}')")
    
    return model, feature_names

def load_saved_model(model_path='heart_model.pkl'):
    """
    Load a previously saved model.
    
    Parameters:
    -----------
    model_path : str
        Path to the saved model file
    
    Returns:
    --------
    model : RandomForestClassifier
        Trained model
    feature_names : list
        List of feature names
    encoder : OrdinalEncoder
        Fitted encoder
    """
    print(f"Loading model from {model_path}...")
    model_data = joblib.load(model_path)
    
    return model_data['model'], model_data['feature_names'], model_data['encoder']

# Example usage
if __name__ == "__main__":
    print("="*60)
    print("Heart Failure Model Training Script")
    print("="*60)
    
    # Option 1: Train and save a new model
    # Uncomment the following lines when you have your heart.csv file
    
    # model, features = train_and_save_model(
    #     csv_path='heart.csv',
    #     model_output='heart_model.pkl'
    # )
    
    # Option 2: Load an existing model
    # model, features, encoder = load_saved_model('heart_model.pkl')
    # print(f"Model loaded with {len(features)} features")
    
    print("\n" + "="*60)
    print("Instructions:")
    print("="*60)
    print("1. Place your 'heart.csv' file in the same directory")
    print("2. Uncomment the train_and_save_model() call above")
    print("3. Run: python model_helper.py")
    print("4. Update app.py to use the saved model")
    print("="*60)
