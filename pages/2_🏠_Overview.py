import streamlit as st
import pandas as pd
import plotly.express as px
from config.config import Config
from utils.styling import load_css

st.set_page_config(page_title="Project Overview", page_icon="📚", layout="wide")
load_css()

st.title("📚 Student's GPA Prediction")

# Project Overview Section
st.markdown("""
## 📖 About This Project
This project leverages **machine learning** to predict students' GPA based on various influential factors. By analyzing features such as **Absences**, **Parental Support**, **Study Time**, and more, the model provides accurate GPA predictions to support data-driven insights in education.

### 📊 Dataset Overview
The dataset comprises detailed information on **2,392 high school students**, capturing their:
- Demographics
- Study habits
- Parental involvement
- Extracurricular activities
- Academic performance

The target variable, **GradeClass**, categorizes students' grades into distinct groups, offering a rich resource for **educational research**, **predictive modeling**, and **statistical analysis**.
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