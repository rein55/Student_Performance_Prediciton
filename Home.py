import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from config.config import Config
from utils.styling import load_css

# Set page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT
)

# Load CSS file
load_css()

# Main title and header
st.title("🎓 My Portfolio with Streamlit")
st.header("🌟 GPA Prediction Made Simple")

# Use CSS classes defined in style.css
st.markdown(
    """
    <div class="highlight">
        Welcome to the **Students' GPA Prediction App**! 🚀 <br>
        Discover insights and predict student performance with ease.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="big-font">
    In this app, you can explore:
    </p>
    <ul>
        <li>📝 Learn more about me by visiting the <b>Profile Page</b>.</li>
        <li>📈 Dive into the <b>Student Performance Dataset</b> and explore valuable insights.</li>
        <li>🔍 Understand the relationships between key features with <i>interactive visualizations</i>.</li>
        <li>🤖 Predict students' GPA using advanced <b>machine learning models</b>.</li>
        <li>📊 Evaluate model performance with intuitive metrics and charts.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    ---
    <h3 class="centered-header">
        🎉 Ready to explore? Use the sidebar to navigate and start your journey!
    </h3>
    """,
    unsafe_allow_html=True
)