import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
from config.config import Config
from utils.styling import load_css

st.set_page_config(page_title="Predictions", page_icon="🔮", layout="wide")

# Load CSS
load_css()

# Initialize session state
if 'predictions' not in st.session_state:
    st.session_state.predictions = []

# Prediction Form
with st.form("prediction_form"):
    st.subheader("Enter Students Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        absences = st.slider(
            "Absences",
            min_value=0,
            max_value=30,
            value=10,
            step=1,  # Menentukan langkah sebagai 1 agar hanya menghasilkan bilangan bulat
            help=Config.FEATURE_DESCRIPTIONS['Absences']
        )
        
        parentalsupport = st.selectbox(
            "Parental Support 0-4 (Low to High)",
            options=[0, 1, 2, 3, 4],
            index=2,  
            help=Config.FEATURE_DESCRIPTIONS['ParentalSupport']
        )
        
        tutoring = st.selectbox(
            "Tutoring 0-1 (No - Yes)",
            options=[0, 1],
            index=0,  
            help=Config.FEATURE_DESCRIPTIONS['Tutoring']
        )
    
    with col2:
        studytimeweekly = st.slider(
            "Study Time Weekly",
            min_value=0.0,
            max_value=20.0,
            value=15.0,
            help=Config.FEATURE_DESCRIPTIONS['StudyTimeWeekly']
        )
        
        extracurricular = st.selectbox(
            "Extracurricular 0-1 (No - Yes)",
            options=[0, 1],
            index=0,  
            help=Config.FEATURE_DESCRIPTIONS['Extracurricular']
        )
        
        music = st.selectbox(
            "Music 0-1 (No - Yes)",
            options=[0, 1],
            index=0,  
            help=Config.FEATURE_DESCRIPTIONS['Music']
        )
    
    with col3:
        sports = st.selectbox(
            "Sports 0-1 (No - Yes)",
            options=[0, 1],
            index=0,  
            help=Config.FEATURE_DESCRIPTIONS['Sports']
        )
        
        ethnicity = st.selectbox(
            "Ethnicity 0-3, 0:(Caucasian), 1:(African American), 2:(Asian), and 3:(Other)",
            options=[0, 1, 2, 3],
            index=2,  
            help=Config.FEATURE_DESCRIPTIONS['Ethnicity']
        )
    
    submitted = st.form_submit_button("🏠 Predict GPA")

if submitted:
    input_data = {
        "Absences": absences,
        "ParentalSupport": parentalsupport,
        "Tutoring": tutoring,
        "StudyTimeWeekly": studytimeweekly,
        "Extracurricular": extracurricular,
        "Music": music,
        "Sports": sports,
        "Ethnicity": ethnicity
    }

# Update API endpoint URL untuk Docker
# API_URL = "http://fastapi:8000"  # Gunakan nama service dari docker-compose
    
    try:
        with st.spinner('Making prediction...'):
            response = requests.post(
                "http://localhost:8000/predict",
                json=input_data
            )
            
            #--- Jika pake docker ---
            # # Update prediction request
            # response = requests.post(
            #     f"{API_URL}/predict",
            #     json=input_data
            # )
            
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                
                # Store prediction
                st.session_state.predictions.append({
                    "prediction": prediction,
                    **input_data
                })
                
                st.success(f"### Predicted Students GPA: {prediction:,.2f}")
                
                # Display feature values
                st.subheader("Feature Values Used")
                feature_df = pd.DataFrame([input_data]).T
                feature_df.columns = ['Value']
                st.dataframe(feature_df)
                
            else:
                st.error(f"Error making prediction: {response.text}")
                
    except requests.exceptions.ConnectionError:
        st.error("Error connecting to the prediction service. Please make sure the API is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display prediction history
if st.session_state.predictions:
    st.header("Prediction History")
    
    df_pred = pd.DataFrame(st.session_state.predictions)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent Predictions")
        for idx, pred in enumerate(df_pred.tail(5).iloc[::-1].to_dict('records')):
            with st.expander(f"Prediction {len(df_pred) - idx}", expanded=idx == 0):
                cols = st.columns(4)
                with cols[0]:
                    st.metric("GPA", f"{pred['prediction']:,.2f}")
                with cols[1]:
                    st.metric("Absences", f"{pred['Absences']:.0f}")
                with cols[2]:
                    st.metric("Parental Support", f"{pred['ParentalSupport']:.0f}")
                with cols[3]:
                    st.metric("Study Time Weekly", f"{pred['StudyTimeWeekly']:.2f}")
    
    with col2:
        if st.button("Clear Prediction History"):
            st.session_state.predictions = []
            st.experimental_rerun()
    
    # Visualization section
    st.header("Prediction Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot of predictions vs rooms
        fig1 = px.scatter(
            df_pred,
            x='Absences',
            y='prediction',
            title='Predicted GPA vs Number of Absences',
            labels={
                'Absences': 'Number of Absences',
                'prediction': 'Predicted GPA'
            }
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.box(
            df_pred,
            x='ParentalSupport',  # Menggunakan nilai asli tanpa binning
            y='prediction',
            title='GPA Distribution by Parental Support',
            labels={
                'ParentalSupport': 'Parental Support',
                'prediction': 'Predicted GPA'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    
    # Statistics
    st.subheader("Prediction Statistics")
    stats_cols = st.columns(4)
    
    with stats_cols[0]:
        st.metric("Average GPA", f"{df_pred['prediction'].mean():,.2f}")
    with stats_cols[1]:
        st.metric("Highest GPA", f"{df_pred['prediction'].max():,.2f}")
    with stats_cols[2]:
        st.metric("Lowest GPA", f"{df_pred['prediction'].min():,.2f}")
    with stats_cols[3]:
        st.metric("Total Predictions", len(df_pred))
    
    # Download predictions
    if not df_pred.empty:
        st.download_button(
            label="Download Prediction History",
            data=df_pred.to_csv(index=False).encode('utf-8'),
            file_name="GPA_predictions.csv",
            mime="text/csv"
        )

else:
    st.info("No predictions made yet. Use the form above to make predictions.")

# Footer
st.markdown("---")