# Student Performance Prediction 🏠

## Project Overview

This project demonstrates an end-to-end machine learning application for predicting student performance. It combines FastAPI for the backend service and Streamlit for an interactive frontend interface.


## Features
- 🔍 Interactive data exploration and visualization
- 📊 Comprehensive model analytics and performance metrics
- 🤖 Real-time student performance using XGBoost
- 📈 Feature importance analysis
- 🎯 Model performance tracking
- 🖥️ User-friendly web interface

## Technology Stack
- **Backend**: FastAPI, Python 3.9
- **Frontend**: Streamlit
- **ML Framework**: Scikit-learn, XGBoost
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Containerization**: Docker
- **Version Control**: Git
- **Development**: VS Code

## Project Structure
```plaintext
Student_Performance_Prediciton/
│
├── .streamlit/                      # Streamlit configuration
│   └── config.toml                  # Streamlit settings
│
├── artifacts/                              # Model artifacts
│   ├── Student_performance_data _.csv      # Dataset
│   ├── best_model.pkl                      # Trained model
│   ├── scaler.pkl                          # Fitted scaler
│   └── metrics.json                        # Model metrics
│
├── config/                          # Configuration
│   ├── __init__.py
│   └── config.py                   # Project configuration
│
├── logs/                           # Application logs
│   └── app.log
│
├── pages/                          # Streamlit pages
│   ├── 1_👤_Profile.py             # Project overview
│   ├── 2_🏠_Overview.py            # Developer profile
│   ├── 3_📊_Analytics.py           # Data analytics
│   └── 4_🔮_Predictions.py         # Student performance predictions
│
├── src/                            # Source code
│   ├── __init__.py
│   ├── data_preparation.py         # Data preprocessing
│   ├── evaluation.py               # Model evaluation
│   └── model.py                    # Model training
│
├── static/                         # Static files
│   ├── css/
│   │   └── style.css              # Custom styling
│   └── img/
│       ├── profile.jpg            # Profile image
│       └── project.png            # Project diagram
│
├── utils/                          # Utilities
│   ├── __init__.py
│   ├── logger.py                   # Logging setup
│   └── styling.py                  # Styling utilities
│
├── app.py                          # FastAPI application
├── Home.py                         # Streamlit main page
├── Dockerfile.fastapi              # FastAPI Dockerfile
├── Dockerfile.streamlit            # Streamlit Dockerfile
├── docker-compose.yml              # Docker composition
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- Docker and Docker Compose
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Student_Performance_Prediciton.git
cd Student_Performance_Prediciton
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows
.\venv\Scripts\activate
# For Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Train the model:
```bash
python train.py
```

5. Run the applications:
```bash
# Terminal 1 - Run FastAPI
uvicorn app:app --reload --port 8000

# Terminal 2 - Run Streamlit
streamlit run Home.py
```

### Docker Setup

#### Building Individual Images

1. FastAPI Image:
```bash
# Build FastAPI image
docker build -t gpa-fastapi:latest -f Dockerfile.fastapi .

# Run FastAPI container
docker run -d -p 8000:8000 --name gpa-fastapi gpa-fastapi:latest
```

2. Streamlit Image:
```bash
# Build Streamlit image
docker build -t gpa-streamlit:latest -f Dockerfile.streamlit .

# Run Streamlit container
docker run -d -p 8501:8501 --name gpa-streamlit gpa-streamlit:latest
```

3. Running with Network:
```bash
# Create network
docker network create gpa-network

# Run FastAPI with network
docker run -d -p 8000:8000 --name gpa-fastapi --network gpa-network gpa-fastapi:latest

# Run Streamlit with network
docker run -d -p 8501:8501 --name gpa-streamlit --network gpa-network gpa-streamlit:latest
```

### Using Docker Compose

1. Build and run services:
```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

2. Stop services:
```bash
docker-compose down
```

## Usage Guide

### Web Interface
1. Access the Streamlit interface at `http://localhost:8501`
2. Navigate through the pages:
   - Profile: Developer information
   - Overview: Project information and dataset exploration
   - Analytics: Model performance and data analysis
   - Predictions: Make real-time predictions

### API Endpoints
Base URL: `http://localhost:8000`

1. Predict Student GPA:
```bash
POST /predict
Content-Type: application/json

{
    'Absences': 5,
    'ParentalSupport': 2,
    'Tutoring': 1,
    'StudyTimeWeekly': 11.25,
    'Extracurricular': 1,
    'Music': 1,
    'Sports': 0,
    'Ethnicity': 2
}
```

2. API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Model Information

### Dataset
- **Source**: Student Performance Dataset
- **Features**: 8 key student data attributes
- **Target**: GPA value of students

### Model Details
- **Algorithm**: XGBoost Regressor
- **Preprocessing**: MinMaxScaler
- **Validation**: 5-fold cross-validation
- **Metrics**: R² Score, RMSE, MAE

## Docker Commands Reference

### Container Management
```bash
# List containers
docker ps

# Stop containers
docker stop gpa-fastapi gpa-streamlit

# Remove containers
docker rm gpa-fastapi gpa-streamlit
```

### Image Management
```bash
# List images
docker images

# Remove images
docker rmi gpa-fastapi:latest gpa-streamlit:latest
```

### Logs and Debugging
```bash
# View logs
docker logs gpa-fastapi
docker logs gpa-streamlit

# Follow logs
docker logs -f gpa-fastapi
```

## Troubleshooting

### Common Issues

1. Port Conflicts
```bash
# Check port usage
lsof -i :8000
lsof -i :8501

# Use alternative ports
docker run -d -p 8001:8000 gpa-fastapi:latest
```

2. Permission Issues
```bash
# Run with sudo (Linux)
sudo docker-compose up

# Add user to docker group
sudo usermod -aG docker $USER
```

3. Memory Issues
```bash
# View resource usage
docker stats

# Set memory limits
docker run -d -p 8000:8000 --memory=1g gpa-fastapi:latest
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Team
- **Rein L Tobing** - Data Scientist
  - Email: reinltobing@gmail.com
  - LinkedIn: [Rein L Tobing](https://www.linkedin.com/in/rein-l-tobing/)
  - GitHub: [rein55](https://github.com/rein55)

## Acknowledgments
- Student Performance Dataset contributors
- Streamlit and FastAPI communities
- XGBoost development team

---
📫 For support, email reinltobing@gmail.com or create an issue in the repository.

Built with ❤️ using Python, FastAPI, and Streamlit