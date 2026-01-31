"""
Machine Learning model for network intrusion detection
Uses Random Forest classifier for binary classification (normal vs attack)
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.preprocessor import TrafficPreprocessor
import config


class IDSModel:
    """Intrusion Detection System ML Model"""
    
    def __init__(self):
        self.model = None
        self.preprocessor = TrafficPreprocessor()
        self.feature_names = None
        self.trained = False
    
    def train(self, training_data_path, test_size=0.2, random_state=42):
        """
        Train the Random Forest model
        
        Args:
            training_data_path: Path to training CSV file
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
        """
        print("=" * 60)
        print("TRAINING IDS MACHINE LEARNING MODEL")
        print("=" * 60)
        
        # Load training data
        print(f"\n1. Loading training data from: {training_data_path}")
        df = pd.read_csv(training_data_path)
        print(f"   ✓ Loaded {len(df)} samples")
        print(f"   ✓ Features: {len(df.columns) - 1}")
        
        # Check label distribution
        label_counts = df['label'].value_counts()
        print(f"\n2. Label distribution:")
        for label, count in label_counts.items():
            print(f"   - {label}: {count} ({count/len(df)*100:.1f}%)")
        
        # Prepare features and labels
        print(f"\n3. Preprocessing data...")
        X = df.drop('label', axis=1)
        y = df['label']
        
        # Fit preprocessor and transform
        X_processed = self.preprocessor.fit_transform(X)
        self.feature_names = X_processed.columns.tolist()
        
        # Convert labels to binary (0 = normal, 1 = attack)
        y_binary = (y == 'attack').astype(int)
        
        print(f"   ✓ Preprocessed {len(X_processed)} samples")
        print(f"   ✓ Feature dimensions: {X_processed.shape}")
        
        # Split data
        print(f"\n4. Splitting data (test size: {test_size})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y_binary, test_size=test_size, 
            random_state=random_state, stratify=y_binary
        )
        print(f"   ✓ Training set: {len(X_train)} samples")
        print(f"   ✓ Test set: {len(X_test)} samples")
        
        # Train Random Forest
        print(f"\n5. Training Random Forest classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            verbose=0
        )
        
        self.model.fit(X_train, y_train)
        print(f"   ✓ Model trained successfully")
        
        # Evaluate model
        print(f"\n6. Evaluating model performance...")
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n   Accuracy: {accuracy * 100:.2f}%")
        
        print(f"\n   Classification Report:")
        print("   " + "-" * 50)
        report = classification_report(y_test, y_pred, 
                                       target_names=['Normal', 'Attack'],
                                       digits=3)
        for line in report.split('\n'):
            print(f"   {line}")
        
        print(f"\n   Confusion Matrix:")
        print("   " + "-" * 50)
        cm = confusion_matrix(y_test, y_pred)
        print(f"   [[TN={cm[0][0]}, FP={cm[0][1]}],")
        print(f"    [FN={cm[1][0]}, TP={cm[1][1]}]]")
        
        # Feature importance
        print(f"\n7. Top 10 Most Important Features:")
        print("   " + "-" * 50)
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in feature_importance.head(10).iterrows():
            print(f"   {row['feature']:25s} : {row['importance']:.4f}")
        
        self.trained = True
        print(f"\n{'=' * 60}")
        print("✓ MODEL TRAINING COMPLETED SUCCESSFULLY")
        print("=" * 60)
    
    def predict(self, features):
        """
        Predict if traffic is normal or attack
        
        Args:
            features: Dictionary or DataFrame of traffic features
        
        Returns:
            Dictionary with prediction and confidence
        """
        if not self.trained:
            raise ValueError("Model must be trained before prediction")
        
        # Preprocess features
        if isinstance(features, dict):
            X = self.preprocessor.preprocess_single(features)
            X = X.reshape(1, -1)
        else:
            X = self.preprocessor.transform(features)
        
        # Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Get confidence (probability of predicted class)
        confidence = probabilities[prediction]
        
        # Convert to label
        label = 'attack' if prediction == 1 else 'normal'
        
        return {
            'prediction': label,
            'confidence': float(confidence),
            'probabilities': {
                'normal': float(probabilities[0]),
                'attack': float(probabilities[1])
            }
        }
    
    def save(self, model_path, scaler_path):
        """Save trained model and preprocessor"""
        if not self.trained:
            raise ValueError("Model must be trained before saving")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✓ Model saved to: {model_path}")
        
        # Save preprocessor
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.preprocessor, f)
        print(f"✓ Preprocessor saved to: {scaler_path}")
    
    def load(self, model_path, scaler_path):
        """Load trained model and preprocessor"""
        # Load model
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✓ Model loaded from: {model_path}")
        
        # Load preprocessor
        with open(scaler_path, 'rb') as f:
            self.preprocessor = pickle.load(f)
        print(f"✓ Preprocessor loaded from: {scaler_path}")
        
        self.trained = True
        self.feature_names = self.preprocessor.numerical_columns


def train_and_save_model():
    """Train model and save to disk"""
    model = IDSModel()
    
    # Train model
    model.train(
        training_data_path=config.TRAINING_DATA_PATH,
        test_size=0.2,
        random_state=42
    )
    
    # Save model
    model.save(
        model_path=config.TRAINED_MODEL_PATH,
        scaler_path=config.SCALER_PATH
    )
    
    return model


def load_trained_model():
    """Load pre-trained model from disk"""
    model = IDSModel()
    
    if os.path.exists(config.TRAINED_MODEL_PATH) and os.path.exists(config.SCALER_PATH):
        model.load(
            model_path=config.TRAINED_MODEL_PATH,
            scaler_path=config.SCALER_PATH
        )
        return model
    else:
        raise FileNotFoundError("Trained model not found. Please train the model first.")


if __name__ == '__main__':
    # Train and save model
    train_and_save_model()
