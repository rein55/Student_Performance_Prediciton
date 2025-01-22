import os
from pathlib import Path

class Config:
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    ARTIFACTS_DIR = BASE_DIR / "artifacts"
    LOGS_DIR = BASE_DIR / "logs"
    STATIC_DIR = BASE_DIR / "static"
    
    # Data paths
    DATA_PATH = ARTIFACTS_DIR / "Student_performance_data _.csv"
    MODEL_PATH = ARTIFACTS_DIR / "best_model.pkl"
    SCALER_PATH = ARTIFACTS_DIR / "scaler.pkl"
    METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
    FEATURE_IMPORTANCE_PATH = ARTIFACTS_DIR / "feature_importance.json"
    
    # Model parameters
    RANDOM_STATE = 42
    TEST_SIZE = 0.3
    NUM_FEATURES = 8
    TARGET_COLUMN = "GPA"
    
    # Feature columns for model
    FEATURE_COLUMNS = [
        "Absences","ParentalSupport","Tutoring","StudyTimeWeekly",
        "Extracurricular","Music","Sports","Ethnicity"
    ]
    
    # Model hyperparameters
    PARAMS = {
        'regressor__max_depth': [3, 4, 5, 6, 7, 8, 9, 10],
        'regressor__learning_rate': [0.001, 0.01, 0.1],
        'regressor__n_estimators': [100, 200, 300],
        'regressor__min_child_weight': [1, 3, 5],
        'regressor__gamma': [0, 0.1, 0.2],
        'regressor__subsample': [0.8, 0.9, 1.0]
    }
    
    # Cross validation settings
    CV_FOLDS = 5
    
    # Logging configuration
    LOG_FILE = LOGS_DIR / "app.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    
    # FastAPI settings
    API_TITLE = "Students GPA Prediction API"
    API_DESCRIPTION = "API for Students GPA Prediction using the Student Performance Dataset"
    API_VERSION = "1.0.0"
    HOST = "0.0.0.0"
    PORT = 8000
    
    # Streamlit settings
    STREAMLIT_PORT = 8501
    PAGE_TITLE = "Students GPA Prediction"
    PAGE_ICON = "📚"
    LAYOUT = "wide"
    
    # Cache settings
    CACHE_TTL = 3600  # 1 hour
    
    # Feature descriptions for documentation
    FEATURE_DESCRIPTIONS = {
        "StudentID": "A unique identifier assigned to each student (1001 to 3392)",
        "Age": "The age of the students ranges from 15 to 18 years",
        "Gender": "Gender of the students, where 0 represents Male and 1 represents Female",
        "Ethnicity": "The ethnicity of the students is coded as 0 (Caucasian), 1 (African American), 2 (Asian), and 3 (Other)",
        "ParentalEducation": "The education level of the parents is coded as 0 (None), 1 (High School), 2 (Some College), 3 (Bachelor's), and 4 (Higher)",
        "StudyTimeWeekly": "Weekly study time in hours, ranging from 0 to 20",
        "Absences": "Number of absences during the school year, ranging from 0 to 30",
        "Tutoring": "Tutoring status, where 0 indicates No and 1 indicates Yes",
        "ParentalSupport": "The level of parental support is coded as 0 (None), 1 (Low), 2 (Moderate), 3 (High), and 4 (Very High).",
        "Extracurricular": "Participation in extracurricular activities, where 0 indicates No and 1 indicates Yes",
        "Sports": "Participation in sports, where 0 indicates No and 1 indicates Yes",
        "Music": "Participation in music activities, where 0 indicates No and 1 indicates Yes",
        "Volunteering": "Participation in volunteering, where 0 indicates No and 1 indicates Yes",
        "GPA": "Grade Point Average on a scale from 2.0 to 4.0, influenced by study habits, parental involvement, and extracurricular activities",
        "GradeClass": "The classification of students' grades based on GPA is coded as 0 ('A' for GPA ≥ 3.5), 1 ('B' for 3.0 ≤ GPA < 3.5), 2 ('C' for 2.5 ≤ GPA < 3.0), 3 ('D' for 2.0 ≤ GPA < 2.5), and 4 ('F' for GPA < 2.0)s"
    }
    
    # Model performance thresholds
    METRIC_THRESHOLDS = {
        'r2_score': 0.8,
        'mae': 3.0,
        'rmse': 4.0
    }
    
    # Data validation rules
    DATA_VALIDATION = {
        'Absences': {'min': 0, 'max': 30},
        'ParentalSupport': {'min': 0, 'max': 4},
        'Tutoring': {'min': 0, 'max': 1},
        'StudyTimeWeekly': {'min': 0, 'max': 20},
        'Extracurricular': {'min': 0, 'max': 1},
        'Music': {'min': 0, 'max': 1},
        'Sports': {'min': 0, 'max': 1},
        'Ethnicity': {'min': 0, 'max': 3}
    }
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        directories = [cls.ARTIFACTS_DIR, cls.LOGS_DIR, cls.STATIC_DIR]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_feature_range(cls, feature):
        """Get the valid range for a feature."""
        return cls.DATA_VALIDATION.get(feature, {'min': float('-inf'), 'max': float('inf')})
    
    @classmethod
    def is_valid_feature_value(cls, feature, value):
        """Check if a feature value is within valid range."""
        ranges = cls.get_feature_range(feature)
        return ranges['min'] <= value <= ranges['max']

# Create directories on import
Config.create_directories()