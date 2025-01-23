import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from config.config import Config
import json
from utils.styling import load_css

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

load_css()

# Load and cache data with proper cache decorator
@st.cache_data(ttl=3600)
def load_data():
    """Load and cache the dataset"""
    try:
        return pd.read_csv(Config.DATA_PATH)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data(ttl=3600)
def load_model_artifacts():
    """Load and cache model metrics and feature importance"""
    try:
        metrics = None
        feature_importance = None
        
        # Load metrics if available
        if Config.METRICS_PATH.exists():
            with open(Config.METRICS_PATH, 'r') as f:
                metrics = json.load(f)
        
        # Load feature importance if available
        if Config.FEATURE_IMPORTANCE_PATH.exists():
            with open(Config.FEATURE_IMPORTANCE_PATH, 'r') as f:
                feature_importance = json.load(f)
                
        return metrics, feature_importance
    except Exception as e:
        st.error(f"Error loading model artifacts: {e}")
        return None, None

try:
    # Load data and model artifacts
    df = load_data()
    metrics, feature_importance = load_model_artifacts()

    if df is not None:
        st.title("📊 Data Analytics & Model Performance")

        # Create tabs
        tab1, tab2, tab3 = st.tabs([
            "Data Analysis", 
            "Feature Relationships", 
            "Model Performance"
        ])

        with tab1:
            st.header("Data Distribution Analysis")
            
            feature = st.selectbox(
                "Select Feature",
                Config.FEATURE_COLUMNS
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    df, 
                    x=feature,
                    marginal="box",  # Tetap menampilkan boxplot di margin
                    title=f"Distribution of {feature}",
                    color_discrete_sequence=["#636EFA"],  # Warna histogram
                    template="plotly_white"  # Template untuk tampilan yang bersih
                )

                # Menambahkan pengaturan layout untuk memperbaiki tampilan
                fig.update_layout(
                    title=dict(
                        text=f"Distribution of {feature}",  # Judul grafik
                        font=dict(size=35)  # Ukuran font judul
                    ),
                    xaxis_title=f"{feature}",  # Label sumbu X
                    yaxis_title="Count",  # Label sumbu Y
                    bargap=0.1,  # Memberikan jarak antar bar
                    font=dict(size=14),  # Ukuran font umum
                    showlegend=False  # Sembunyikan legend jika tidak diperlukan
                )

                # Menyesuaikan tampilan boxplot marginal
                fig.update_traces(
                    marker=dict(line=dict(width=1, color="black")),  # Border bar
                    opacity=0.7  # Transparansi histogram
                )

                # Menampilkan grafik di Streamlit
                st.plotly_chart(fig, use_container_width=True)

            
                with col2:
                    # Mengatur ukuran font menggunakan HTML di Markdown
                    st.markdown("<h2 style='font-size:35px;'>Descriptive Statistics</h2>", unsafe_allow_html=True)
                    stats = df[feature].describe()
                    # Tambahkan warna pada output tabel
                    styled_stats = stats.to_frame(name='Values').style.background_gradient(cmap='coolwarm').format("{:.2f}")
                    # Tampilkan tabel di Streamlit
                    st.dataframe(styled_stats, use_container_width=True)
                    
                    # Tambahkan summary tambahan
                    st.info(f"🔢 Total data points: {len(df[feature])}")


        with tab2:
            st.header("Feature Relationships")
            
            # Hitung correlation matrix
            corr = df[Config.FEATURE_COLUMNS + [Config.TARGET_COLUMN]].corr()

            # Buat heatmap dengan anotasi untuk nilai korelasi
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="RdBu",
                zmin=-1, zmax=1,
                colorbar=dict(title="Correlation"),
                hoverongaps=False
            ))

            # Tambahkan anotasi nilai korelasi di setiap sel
            for i in range(len(corr.columns)):
                for j in range(len(corr.columns)):
                    fig.add_annotation(
                        x=corr.columns[i],
                        y=corr.columns[j],
                        text=f"{corr.values[i, j]:.2f}",
                        showarrow=False,
                        font=dict(color="white" if abs(corr.values[i, j]) > 0.5 else "black")
                    )

            # Update layout untuk memperindah tampilan
            fig.update_layout(
                title="Feature Correlation Matrix",
                title_x=0.5,
                xaxis_title="Features",
                yaxis_title="Features",
                template="plotly_white",
                width=500,
                height=500
            )

            # Tampilkan di Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                x_feature = st.selectbox("Select X-axis feature", Config.FEATURE_COLUMNS)
            with col2:
                y_feature = st.selectbox(
                    "Select Y-axis feature", 
                    [Config.TARGET_COLUMN], 
                    index=1 if len([Config.TARGET_COLUMN]) > 1 else 0
                )
            
            fig = px.scatter(
                df,
                x=x_feature,
                y=y_feature,
                title=f"{x_feature} vs {y_feature}",
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.header("Model Performance")
            
            if metrics and feature_importance:
                # Display metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Test R² Score", f"{metrics['test_r2']:.4f}")
                with col2:
                    st.metric("Test RMSE", f"{metrics['test_rmse']:,.2f}")
                with col3:
                    st.metric("Test MAE", f"{metrics['test_mae']:,.2f}")
                
                # Training vs Testing Performance
                # Dataframe untuk tabel metrik
                metrics_df = pd.DataFrame({
                    'Metric': ['R²', 'RMSE', 'MAE'],
                    'Training': [
                        metrics['train_r2'],
                        metrics['train_rmse'],
                        metrics['train_mae']
                    ],
                    'Testing': [
                        metrics['test_r2'],
                        metrics['test_rmse'],
                        metrics['test_mae']
                    ]
                })

                # Tambahkan highlight pada tabel untuk memperjelas
                def highlight_best(value, color="lightblue"):
                    """Highlight values to make them more appealing."""
                    if isinstance(value, (int, float)):
                        return f"background-color: {color};" if value > 0 else ""
                    return ""

                st.subheader("Training vs Testing Performance")

                # Styling tabel
                styled_df = metrics_df.style.format(precision=2).applymap(highlight_best, subset=['Training', 'Testing'])

                # Menampilkan tabel menggunakan st.table
                st.table(styled_df)

                # Feature Importance Section
                st.subheader("Feature Importance Analysis")
                
                # Create DataFrame from feature importance
                importance_df = pd.DataFrame({
                    'Feature': list(feature_importance.keys()),
                    'Importance': list(feature_importance.values())
                }).sort_values('Importance', ascending=True)

                # Create bar chart
                fig = go.Figure(go.Bar(
                    x=importance_df['Importance'],
                    y=importance_df['Feature'],
                    orientation='h',
                    marker=dict(
                        color=importance_df['Importance'],  # Gradient color based on importance
                        colorscale='Viridis',  # Use a vibrant colorscale
                        line=dict(color='rgba(50, 50, 50, 0.6)', width=1)  # Add border for bars
                    ),
                    text=importance_df['Importance'],  # Show values on hover
                    textposition='auto',  # Display values on the bars
                    hoverinfo="text+name"
                ))

                # Update layout for better styling
                fig.update_layout(
                    title=dict(
                        text='Feature Importance Analysis',
                        font=dict(size=20, color='rgb(40,40,40)'),
                        x=0.5,  # Center the title
                    ),
                    xaxis=dict(
                        title='Importance Score',
                        titlefont=dict(size=14),
                        tickfont=dict(size=12),
                        showgrid=True,
                        gridcolor='rgba(200, 200, 200, 0.2)'
                    ),
                    yaxis=dict(
                        title='Features',
                        titlefont=dict(size=14),
                        tickfont=dict(size=12)
                    ),
                    template='plotly_white',
                    height=500,  # Increase height for better readability
                    margin=dict(l=100, r=20, t=60, b=40),  # Adjust margins
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                    plot_bgcolor='rgba(245,245,245,1)'  # Light grey plot area
                )

                # Add reference line for average importance
                avg_importance = importance_df['Importance'].mean()
                fig.add_shape(
                    type="line",
                    x0=avg_importance,
                    y0=-0.5,
                    x1=avg_importance,
                    y1=len(importance_df['Feature']) - 0.5,
                    line=dict(
                        color="red",
                        width=2,
                        dash="dash"
                    ),
                    name="Average"
                )

                # Display chart
                st.plotly_chart(fig, use_container_width=True)

                # Feature Importance Details
                with st.expander("Feature Importance Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### Top Features")
                        top_features = importance_df.tail(3).copy()
                        top_features['Importance(%)'] = top_features['Importance'] * 100
                        top_features = top_features.sort_values('Importance(%)', ascending=False)

                        # Create Plotly table
                        fig = go.Figure(data=[go.Table(
                            header=dict(
                                values=["<b>Feature</b>", "<b>Importance(%)</b>"],
                                fill_color='royalblue',
                                font=dict(color='white', size=14),
                                align='center'
                            ),
                            cells=dict(
                                values=[top_features['Feature'], top_features['Importance(%)'].round(2)],
                                fill_color='lightgray',
                                font=dict(color='black', size=12),
                                align='center'
                            )
                        )])

                        # Update layout
                        fig.update_layout(
                            title="Top Features",
                            title_x=0.5,  # Center title
                            margin=dict(l=10, r=10, t=40, b=10),  # Adjust margins
                            height=300  # Adjust height
                        )

                        # Display Plotly table
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown("### Feature Importance Distribution")
                        # Sunburst Chart
                        fig = px.sunburst(
                            importance_df,
                            path=['Feature'],  # Use 'Feature' as hierarchy
                            values='Importance',
                            title='Feature Importance Distribution'
                        )

                        fig.update_layout(
                            template='plotly_white',
                            height=400
                        )

                        st.plotly_chart(fig, use_container_width=True)


            else:
                st.warning("Model metrics and feature importance not available. Please train the model first.")

except Exception as e:
    st.error(f"Error in analytics: {str(e)}")