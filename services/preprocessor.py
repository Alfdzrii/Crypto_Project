"""
Data preprocessing utilities for network traffic data
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


class TrafficPreprocessor:
    """Preprocessor for network traffic data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.categorical_columns = ['protocol_type', 'service', 'flag']
        self.numerical_columns = None
        self.fitted = False
    
    def fit(self, df):
        """
        Fit the preprocessor on training data
        
        Args:
            df: Training DataFrame
        """
        df_copy = df.copy()
        
        # Encode categorical columns
        for col in self.categorical_columns:
            if col in df_copy.columns:
                le = LabelEncoder()
                df_copy[col] = le.fit_transform(df_copy[col].astype(str))
                self.label_encoders[col] = le
        
        # Get numerical columns (excluding label)
        self.numerical_columns = [col for col in df_copy.columns 
                                  if col != 'label' and df_copy[col].dtype in ['int64', 'float64']]
        
        # Fit scaler on numerical columns
        if self.numerical_columns:
            self.scaler.fit(df_copy[self.numerical_columns])
        
        self.fitted = True
        print("✓ Preprocessor fitted on training data")
    
    def transform(self, df):
        """
        Transform data using fitted preprocessor
        
        Args:
            df: DataFrame to transform
        
        Returns:
            Transformed DataFrame
        """
        if not self.fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        df_copy = df.copy()
        
        # Handle missing values
        df_copy = df_copy.fillna(0)
        
        # Encode categorical columns
        for col in self.categorical_columns:
            if col in df_copy.columns:
                le = self.label_encoders.get(col)
                if le:
                    # Handle unseen categories
                    df_copy[col] = df_copy[col].astype(str).apply(
                        lambda x: x if x in le.classes_ else le.classes_[0]
                    )
                    df_copy[col] = le.transform(df_copy[col])
        
        # Scale numerical columns
        if self.numerical_columns:
            df_copy[self.numerical_columns] = self.scaler.transform(df_copy[self.numerical_columns])
        
        return df_copy
    
    def fit_transform(self, df):
        """Fit and transform in one step"""
        self.fit(df)
        return self.transform(df)
    
    def preprocess_single(self, features_dict):
        """
        Preprocess a single traffic instance
        
        Args:
            features_dict: Dictionary of traffic features
        
        Returns:
            Preprocessed feature array
        """
        # Convert to DataFrame
        df = pd.DataFrame([features_dict])
        
        # Transform
        df_transformed = self.transform(df)
        
        # Remove label if present
        if 'label' in df_transformed.columns:
            df_transformed = df_transformed.drop('label', axis=1)
        
        return df_transformed.values[0]


def prepare_features(df, drop_label=True):
    """
    Prepare features from DataFrame
    
    Args:
        df: Input DataFrame
        drop_label: Whether to drop the label column
    
    Returns:
        Feature matrix (X) and optionally labels (y)
    """
    df_copy = df.copy()
    
    # Handle missing values
    df_copy = df_copy.fillna(0)
    
    # Separate features and labels
    if 'label' in df_copy.columns:
        y = df_copy['label']
        X = df_copy.drop('label', axis=1)
    else:
        y = None
        X = df_copy
    
    if drop_label:
        return X, y
    else:
        return X


def validate_features(features_dict, required_features):
    """
    Validate that all required features are present
    
    Args:
        features_dict: Dictionary of features
        required_features: List of required feature names
    
    Returns:
        Boolean indicating if valid
    """
    missing = [f for f in required_features if f not in features_dict]
    
    if missing:
        print(f"⚠ Missing features: {missing}")
        return False
    
    return True
