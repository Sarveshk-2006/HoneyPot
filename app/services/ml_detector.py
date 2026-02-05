"""
Advanced ML-based scam detection enhancement
Provides machine learning models for improved detection accuracy
"""

import json
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from pathlib import Path

class MLScamDetector:
    """Machine Learning enhanced scam detector"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = TfidfVectorizer(max_features=1000, lowercase=True)
        self.classifier = MultinomialNB()
        self.pipeline = Pipeline([
            ('tfidf', self.vectorizer),
            ('classifier', self.classifier)
        ])
        self.is_trained = False
        self.scam_types = ['banking', 'upi', 'phishing', 'investment', 'romance']
        self.initialize_training_data()
    
    def initialize_training_data(self):
        """Initialize with predefined training data for scam detection"""
        
        training_data = {
            'banking': [
                'your bank account has been compromised',
                'verify your bank details immediately',
                'update your banking information',
                'confirm your account details for security',
                'your account requires immediate verification',
                'reset your banking password now',
                'suspicious activity on your bank account',
                'bank security alert urgent',
                'verify identity with bank details',
                'your bank account is locked',
            ],
            'upi': [
                'send money via upi to secure account',
                'upi payment required for verification',
                'share your upi id for refund',
                'upi transfer needed for confirmation',
                'update upi details for safety',
                'link your upi account now',
                'upi verification required',
                'share upi id with us',
            ],
            'phishing': [
                'click here to verify account',
                'confirm your identity by clicking link',
                'visit this website to complete verification',
                'open this link to secure your account',
                'click to prevent account closure',
                'verify by visiting this website',
                'authenticate yourself through this link',
                'secure your account by clicking here',
            ],
            'investment': [
                'guaranteed returns on investment',
                'invest now get 100% profit',
                'double your money in 30 days',
                'risk free investment opportunity',
                'guaranteed returns investment scheme',
                'make quick money with us',
                'get rich quick with this plan',
                'investment with guaranteed profits',
            ],
            'romance': [
                'i love you lets get married',
                'can you send me money',
                'im in financial trouble help me',
                'transfer money for our future',
                'i need money for emergency',
                'send me gifts online',
                'i miss you send money for ticket',
                'help me with money for travel',
            ]
        }
        
        # Prepare training data
        texts = []
        labels = []
        for scam_type, examples in training_data.items():
            for example in examples:
                texts.append(example)
                labels.append(scam_type)
        
        # Train the model
        if texts:
            self.pipeline.fit(texts, labels)
            self.is_trained = True
    
    def predict_scam_type(self, message: str) -> Tuple[str, float]:
        """
        Predict scam type using ML model
        Returns: (scam_type, confidence)
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        try:
            # Get prediction
            prediction = self.pipeline.predict([message])[0]
            
            # Get prediction probability
            probabilities = self.pipeline.predict_proba([message])[0]
            confidence = float(np.max(probabilities))
            
            return prediction, confidence
        except Exception as e:
            print(f"ML prediction error: {e}")
            return 'unknown', 0.0
    
    def predict_all_probabilities(self, message: str) -> Dict[str, float]:
        """Get probabilities for all scam types"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        try:
            probabilities = self.pipeline.predict_proba([message])[0]
            result = {}
            for scam_type, prob in zip(self.pipeline.classes_, probabilities):
                result[scam_type] = float(prob)
            return result
        except Exception as e:
            print(f"Error getting probabilities: {e}")
            return {scam_type: 0.0 for scam_type in self.scam_types}
    
    def get_feature_importance(self, message: str) -> Dict[str, float]:
        """Get important features (keywords) for prediction"""
        try:
            # Get TF-IDF features
            tfidf_matrix = self.vectorizer.transform([message])
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get non-zero features
            feature_indices = tfidf_matrix.nonzero()[1]
            importance_scores = tfidf_matrix.data
            
            result = {}
            for idx, score in zip(feature_indices, importance_scores):
                feature = feature_names[idx]
                result[feature] = float(score)
            
            # Sort by importance
            return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])
        except Exception as e:
            print(f"Error getting feature importance: {e}")
            return {}

# Initialize global ML detector
ml_detector = MLScamDetector()
