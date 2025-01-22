import streamlit as st
import pandas as pd
import plotly.express as px
from config.config import Config
from utils.styling import load_css

st.set_page_config(page_title="Project Overview", page_icon="📚", layout="wide")
load_css()

st.title("📚 Students GPA Prediction")

# Project Overview Section
st.markdown("""
## About This Project
This project uses machine learning to predict Student GPA based on various features. The model takes into 
account factors like Absences, Parental Support, Study Time, etc to estimate Students GPA.

### Dataset Information
This dataset contains comprehensive information on 2,392 high school students, 
detailing their demographics, study habits, parental involvement, 
extracurricular activities, and academic performance. The target variable, GradeClass, 
classifies students' grades into distinct categories, providing a robust dataset for 
educational research, predictive modeling, and statistical analysis..
""")

# Load and cache data
@st.cache_data
def load_data():
    return pd.read_csv(Config.DATA_PATH)

try:
    df = load_data()
    
    # Dataset Overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", f"{len(df):,}")
    with col2:
        st.metric("Average GPA", f"{df['GPA'].mean():,.2f}")
    with col3:
        st.metric("Features", f"{len(Config.FEATURE_COLUMNS)}")

    # Feature Descriptions
    st.header("📝 Feature Descriptions")
    descriptions = pd.DataFrame.from_dict(
        Config.FEATURE_DESCRIPTIONS, 
        orient='index',
        columns=['Description']
    )
    st.table(descriptions)

    # Data Sample
    with st.expander("View Sample Data"):
        st.dataframe(df.head())

    # Basic Statistics
    st.header("📊 Basic Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("GPA Distribution")
        fig = px.histogram(
            df, 
            x='GPA',
            title="Students GPA Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("GPA by Absences")
        fig = px.box(
            df, 
            x='Absences', 
            y='GPA',
            title="GPA Distribution by Number of Absences"
        )
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")