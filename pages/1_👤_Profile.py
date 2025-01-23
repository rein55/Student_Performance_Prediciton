import streamlit as st
import pandas as pd
from utils.styling import load_css
import base64


def get_pdf_download_link(pdf_path, filename):
    """Generate download link for PDF file"""
    with open(pdf_path, "rb") as f:
        bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-button">📥 Download CV</a>'
    return href

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

load_css()


# Custom CSS
st.markdown("""
    <style>
    .css-1v0mbdj.etr89bj1 {
        text-align: center;
    }
    .profile-img {
        border-radius: 50%;
        margin: 0 auto;
        display: block;
    }
    .social-links {
        text-align: center;
        padding: 1rem 0;
    }
    .experience-card {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        border-left: 3px solid #0366d6;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    # Profile Image
    st.image("static/img/profile.jpg", width=200, output_format="auto")
    
    # Contact Information
    st.markdown("""
    ### Contact
    - 📧 reinltobing@gmail.com
    - 📱 0823 2117 5897
    """)
    
    # Social Links
    st.markdown("""
    ### Social Links
    - [GitHub](https://github.com/rein55)
    - [LinkedIn](https://www.linkedin.com/in/rein-l-tobing)
    """)

with col2:
    st.title("Rein L Tobing")
    st.subheader("Machine Learning Engineer")
    st.markdown(get_pdf_download_link("cv/CV-Rein L Tobing.pdf", "CV-Rein L Tobing.pdf"), unsafe_allow_html=True)
    
    st.markdown("""
    ### Summary
    Driven accountant with over 6 years of experience in accounting and cost accounting, 
    now starting new career in AI and Machine Learning. Skilled in financial reporting, data processing, and optimization, 
    with technical proficiency in Excel, Python, and various machine learning models. Conducted Market Basket Analysis to 
    optimize product placement and increased sales potential by 15%. Reduced processing time for sales verification 
    from 2-3 hours to 10-20 minutes. Known for analytical thinking, problem-solving, and adaptability, 
    I am seeking a full-time position in machine learning engineering or data science to leverage both my financial and technical expertise..
    """)

# Experience Section
st.header("Professional Experience")

experiences = [
    {
        "role": "Accounting Staff",
        "company": "PT Darma Inti Solusi",
        "period": "NOV 2022 – SEPT 2023",
        "points": [
            "Recorded transaction journals and prepared financial statements, optimizing documentation processes to reduce errors by 25% and improve financial reporting transparency.",
            "Inputted, paid, and reported corporate taxes (including income tax and VAT), enhancing compliance efficiency and reducing processing time by 30% through an organized tax and management",
        ]
    },
    {
        "role": "Cost Accounting Staff",
        "company": "PT Malindo Feedmill, Tbk",
        "period": "SEPT 2018 – OCT 2022",
        "points": [
            "Input and checked the farmers' business calculation list by implementing a standardized review process, resulting in a 20% improvement in accuracy and a reduction in calculation errors",
            "Analyzed farmer performance and prepared incentive reports, implementing a clear reporting structure that improved transparency by 30%",
        ]
    }
]

for exp in experiences:
    with st.expander(f"{exp['company']} - {exp['role']}", expanded=True):
        st.markdown(f"**Period:** {exp['period']}")
        for point in exp['points']:
            st.markdown(f"- {point}")

# Skills Section
st.header("Skills & Expertise")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Technical Skills")
    technical_skills = [
        "Machine Learning",
        "Data Analysis ",
        "Data Visualization",
        "Python Programming",
        "Data Visualization"
    ]
    for skill in technical_skills:
        st.markdown(f"- {skill}")

with col2:
    st.subheader("Tools & Technologies")
    tools = [
        "Python",
        "Power BI",
        "TensorFlow",
        "Dockers",
        "MLflow"
    ]
    for tool in tools:
        st.markdown(f"- {tool}")

# Education Section
st.header("Education")
st.markdown("""
#### Institut Digital Ekonomi LPKIA
- **Degree:** Bachelor of Information System
- **GPA:** 3.94/4.00
- **Period:** 2023 - 2024
""")