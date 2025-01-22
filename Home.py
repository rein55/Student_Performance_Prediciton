import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from config.config import Config
from utils.styling import load_css



st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT
)

load_css()

st.title("📚 Students GPA Prediction")
st.markdown("""
Welcome to the Students GPA Prediction App! This application helps you:
- Explore the Student Performance Dataset
- Understand feature relationships
- Make Students GPA predictions using machine learning
- View model performance metrics

Use the navigation menu on the left to explore different sections of the app.
""")

# Load and display sample data
@st.cache_data
def load_data():
    return pd.read_csv(Config.DATA_PATH)

try:
    df = load_data()
    
    # Show dataset overview
    st.header("📊 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Number of Students", df.shape[0])
    with col2:
        st.metric("Average GPA", f"{df['GPA'].mean():,.2f}")
    with col3:
        st.metric("Features Used", len(Config.FEATURE_COLUMNS))
    
    # Show feature descriptions
    st.header("📝 Feature Descriptions")
    descriptions = pd.DataFrame.from_dict(
        Config.FEATURE_DESCRIPTIONS, 
        orient='index',
        columns=['Description']
    )
    st.dataframe(descriptions, use_container_width=True)
    
    # Show sample data
    st.header("🔍 Sample Data")
    st.dataframe(df.head())
    
except Exception as e:
    st.error(f"Error loading data: {str(e)}")