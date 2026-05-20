import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, r2_score

# Set page config
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model():
    with open('student_model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    return pd.read_csv('student_data.csv')

model = load_model()
data = load_data()

# Feature names
feature_names = ['study_hours', 'attendance_percentage', 'previous_score', 
                 'assignments_completed', 'sleep_hours', 'extracurricular_activities', 
                 'daily_internet_usage']

# Sidebar navigation
st.sidebar.markdown("# 📚 Navigation")
page = st.sidebar.radio("Select a page:", 
                        ["🏠 Home", "🔮 Predict Performance", "📊 Data Analysis", "📈 Model Insights"])

# ============= HOME PAGE =============
if page == "🏠 Home":
    st.markdown('<p class="header-title">Student Performance Predictor</p>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ## Welcome! 👋
        
        This application predicts student final scores based on various academic and lifestyle factors.
        
        ### Key Features:
        - **Predict Performance**: Input student metrics to get predicted final score
        - **Data Analysis**: Explore relationships between factors and performance
        - **Model Insights**: Understand feature importance and model accuracy
        
        ### Factors Considered:
        - 📖 Study Hours
        - 📍 Attendance Percentage
        - 📚 Previous Score
        - ✅ Assignments Completed
        - 😴 Sleep Hours
        - 🎭 Extracurricular Activities
        - 🌐 Daily Internet Usage
        """)
    
    with col2:
        st.info("""
        ### Quick Stats
        
        **Dataset Overview:**
        - Total Students: 200
        - Features Analyzed: 7
        - Prediction Range: 0-100
        
        **Model Type:** Linear Regression
        
        **Model Performance:**
        - R² Score: Calculated on prediction page
        - MAE: Displayed in model insights
        """)
    
    # Display sample data
    st.markdown("### 📋 Sample Data")
    st.dataframe(data.head(10), use_container_width=True)

# ============= PREDICTION PAGE =============
elif page == "🔮 Predict Performance":
    st.markdown('<p class="header-title">Predict Student Performance</p>', 
                unsafe_allow_html=True)
    
    st.markdown("Enter student details to predict their final score:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📖 Study & Learning")
        study_hours = st.slider("Study Hours (0-10)", 0.0, 10.0, 5.0, 0.1)
        previous_score = st.slider("Previous Score (0-100)", 0, 100, 70)
        assignments_completed = st.slider("Assignments Completed (0-100)", 0, 100, 50)
    
    with col2:
        st.subheader("🎓 Attendance & Activities")
        attendance_percentage = st.slider("Attendance Percentage (0-100)", 0, 100, 75)
        extracurricular_activities = st.slider("Extracurricular Activities (0-10)", 0, 10, 5)
        sleep_hours = st.slider("Sleep Hours (0-10)", 0.0, 10.0, 7.0, 0.1)
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💻 Daily Habits")
        daily_internet_usage = st.slider("Daily Internet Usage (0-10 hours)", 0.0, 10.0, 5.0, 0.1)
    
    with col4:
        st.subheader("")
        st.write("")
        predict_button = st.button("🎯 Predict Final Score", use_container_width=True)
    
    if predict_button:
        # Prepare input
        input_data = np.array([[
            study_hours,
            attendance_percentage,
            previous_score,
            assignments_completed,
            sleep_hours,
            extracurricular_activities,
            daily_internet_usage
        ]])
        
        # Make prediction
        predicted_score = model.predict(input_data)[0]
        
        # Display result
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Determine color based on score
            if predicted_score >= 90:
                color = "🟢"
                grade = "A+"
            elif predicted_score >= 80:
                color = "🟢"
                grade = "A"
            elif predicted_score >= 70:
                color = "🟡"
                grade = "B"
            elif predicted_score >= 60:
                color = "🟠"
                grade = "C"
            else:
                color = "🔴"
                grade = "D"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 15px; color: white;">
                <h2>Predicted Final Score</h2>
                <h1 style="font-size: 4em; margin: 20px 0;">{predicted_score:.1f}/100</h1>
                <h3>{color} Grade: {grade}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Show breakdown and recommendations
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Input Summary")
            summary_df = pd.DataFrame({
                'Factor': feature_names,
                'Value': [study_hours, attendance_percentage, previous_score, 
                         assignments_completed, sleep_hours, extracurricular_activities, 
                         daily_internet_usage]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("💡 Recommendations")
            recommendations = []
            
            if study_hours < 5:
                recommendations.append("📚 Increase study hours for better performance")
            if attendance_percentage < 80:
                recommendations.append("📍 Improve attendance - aim for 80%+")
            if previous_score < 60:
                recommendations.append("📈 Focus on fundamentals from previous concepts")
            if assignments_completed < 75:
                recommendations.append("✅ Complete more assignments for better grades")
            if sleep_hours < 6:
                recommendations.append("😴 Get more sleep - aim for 6-8 hours")
            if daily_internet_usage > 7:
                recommendations.append("⏱️ Reduce internet usage for better focus")
            
            if recommendations:
                for rec in recommendations:
                    st.info(rec)
            else:
                st.success("✨ Great job! Keep up the good habits!")

# ============= DATA ANALYSIS PAGE =============
elif page == "📊 Data Analysis":
    st.markdown('<p class="header-title">Data Analysis & Insights</p>', 
                unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Distributions", "🔗 Correlations", "🎯 Feature Comparison"])
    
    with tab1:
        st.subheader("Distribution of Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data['final_score'], bins=20, color='#667eea', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Final Score', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Final Scores', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data['study_hours'], bins=20, color='#764ba2', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Study Hours', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Study Hours', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data['attendance_percentage'], bins=20, color='#f093fb', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Attendance %', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Attendance', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        with col4:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data['sleep_hours'], bins=20, color='#4facfe', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Sleep Hours', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Sleep Hours', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Feature Correlations with Final Score")
        
        # Calculate correlations
        correlations = data[feature_names + ['final_score']].corr()['final_score'][:-1].sort_values(ascending=False)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Bar plot of correlations
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['green' if x > 0 else 'red' for x in correlations.values]
            ax.barh(range(len(correlations)), correlations.values, color=colors, alpha=0.7, edgecolor='black')
            ax.set_yticks(range(len(correlations)))
            ax.set_yticklabels(correlations.index)
            ax.set_xlabel('Correlation with Final Score', fontsize=12)
            ax.set_title('Feature Correlations', fontsize=14, fontweight='bold')
            ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            st.dataframe(
                correlations.to_frame(name='Correlation with Final Score').reset_index()
                .rename(columns={'index': 'Feature'}),
                use_container_width=True,
                hide_index=True
            )
        
        # Correlation heatmap
        st.subheader("Full Correlation Matrix")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(data[feature_names + ['final_score']].corr(), 
                    annot=True, fmt='.2f', cmap='coolwarm', center=0,
                    square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Feature Relationships with Final Score")
        
        selected_feature = st.selectbox("Select a feature to visualize:", feature_names)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter(data[selected_feature], data['final_score'], alpha=0.6, s=80, color='#667eea', edgecolor='black')
        
        # Add trend line
        z = np.polyfit(data[selected_feature], data['final_score'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(data[selected_feature].min(), data[selected_feature].max(), 100)
        ax.plot(x_trend, p(x_trend), "r--", linewidth=2, label='Trend line')
        
        ax.set_xlabel(selected_feature.replace('_', ' ').title(), fontsize=12)
        ax.set_ylabel('Final Score', fontsize=12)
        ax.set_title(f'Relationship: {selected_feature.replace("_", " ").title()} vs Final Score', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)

# ============= MODEL INSIGHTS PAGE =============
elif page == "📈 Model Insights":
    st.markdown('<p class="header-title">Model Performance & Insights</p>', 
                unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Performance Metrics", "🔬 Feature Importance", "✔️ Predictions vs Actual"])
    
    with tab1:
        st.subheader("Model Evaluation Metrics")
        
        # Make predictions on full dataset
        X = data[feature_names]
        y = data['final_score']
        y_pred = model.predict(X)
        
        # Calculate metrics
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(np.mean((y - y_pred) ** 2))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("R² Score", f"{r2:.4f}", 
                     help="Proportion of variance explained (0-1, higher is better)")
        
        with col2:
            st.metric("MAE (Mean Absolute Error)", f"{mae:.2f}", 
                     help="Average absolute difference between predicted and actual scores")
        
        with col3:
            st.metric("RMSE", f"{rmse:.2f}", 
                     help="Root Mean Squared Error")
        
        # Model information
        st.markdown("---")
        st.subheader("Model Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Model Type:** Linear Regression
            
            **Training Data:**
            - Samples: {len(data)}
            - Features: {len(feature_names)}
            
            **Performance Summary:**
            - The model explains {r2*100:.2f}% of the variance in final scores
            - Average prediction error: ±{mae:.2f} points
            """)
        
        with col2:
            # Create a simple distribution plot of residuals
            residuals = y - y_pred
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(residuals, bins=20, color='#667eea', edgecolor='black', alpha=0.7)
            ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero Error')
            ax.set_xlabel('Residuals (Actual - Predicted)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Prediction Errors', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Feature Importance Analysis")
        
        # Get model coefficients
        coefficients = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model.coef_
        }).sort_values('Coefficient', ascending=False)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#667eea' if x > 0 else '#f093fb' for x in coefficients['Coefficient']]
            ax.barh(range(len(coefficients)), coefficients['Coefficient'], color=colors, alpha=0.7, edgecolor='black')
            ax.set_yticks(range(len(coefficients)))
            ax.set_yticklabels([f.replace('_', ' ').title() for f in coefficients['Feature']])
            ax.set_xlabel('Coefficient Value', fontsize=12)
            ax.set_title('Feature Coefficients (Impact on Score)', fontsize=14, fontweight='bold')
            ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            st.dataframe(
                coefficients.reset_index(drop=True)
                .assign(**{'Feature': coefficients['Feature'].str.replace('_', ' ').str.title()}),
                use_container_width=True,
                hide_index=True
            )
        
        st.info("""
        **Interpretation:**
        - **Positive coefficients**: Features that increase the final score
        - **Negative coefficients**: Features that decrease the final score
        - **Magnitude**: Larger absolute values = stronger impact on predictions
        """)
    
    with tab3:
        st.subheader("Actual vs Predicted Scores")
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.scatter(y, y_pred, alpha=0.6, s=80, color='#667eea', edgecolor='black')
            
            # Perfect prediction line
            min_val = min(y.min(), y_pred.min())
            max_val = max(y.max(), y_pred.max())
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
            
            ax.set_xlabel('Actual Final Score', fontsize=12)
            ax.set_ylabel('Predicted Final Score', fontsize=12)
            ax.set_title('Actual vs Predicted Scores', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            # Summary statistics
            st.metric("Predictions within ±5 points", 
                     f"{sum(abs(residuals) <= 5)}/{len(y)} ({100*sum(abs(residuals) <= 5)/len(y):.1f}%)")
            st.metric("Predictions within ±10 points", 
                     f"{sum(abs(residuals) <= 10)}/{len(y)} ({100*sum(abs(residuals) <= 10)/len(y):.1f}%)")
            
            st.markdown("---")
            
            # Show some example predictions
            comparison_df = pd.DataFrame({
                'Actual': y.values[:10],
                'Predicted': y_pred[:10].astype(int),
                'Error': (y - y_pred).values[:10].astype(int)
            })
            
            st.subheader("Sample Predictions")
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px; padding: 20px;">
    <p>📚 Student Performance Predictor | Built with Streamlit & Linear Regression</p>
    <p>© 2024 | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
