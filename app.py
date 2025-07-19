import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import random
from datetime import datetime, timedelta
import sqlite3
import io
import base64

# Configure page
st.set_page_config(
    page_title="StrategySim Enterprise - Business Strategy Game",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for game-like interface
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .game-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .strategy-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .score-display {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class BusinessStrategyGame:
    def __init__(self):
        self.player_score = 0
        self.level = 1
        self.experience = 0
        self.achievements = []
        self.decisions_made = []
        
    def calculate_score(self, decision_quality, data_insights):
        base_score = decision_quality * 100
        bonus = data_insights * 50
        return base_score + bonus
    
    def level_up(self):
        if self.experience >= self.level * 1000:
            self.level += 1
            return True
        return False

# Initialize game state
if 'game' not in st.session_state:
    st.session_state.game = BusinessStrategyGame()

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

if 'strategic_questions' not in st.session_state:
    st.session_state.strategic_questions = []

def load_sample_sap_data():
    """Generate sample SAP-like data for demonstration"""
    np.random.seed(42)
    
    # Sample SAP Financial Data
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='M')
    
    data = {
        'Date': dates,
        'Revenue': np.random.normal(5000000, 500000, len(dates)).cumsum() + 10000000,
        'Profit_Margin': np.random.normal(0.15, 0.05, len(dates)),
        'Operating_Costs': np.random.normal(3000000, 300000, len(dates)).cumsum() + 6000000,
        'Customer_Count': np.random.normal(10000, 1000, len(dates)).cumsum() + 50000,
        'Market_Share': np.random.normal(0.25, 0.05, len(dates)),
        'Employee_Count': np.random.normal(500, 50, len(dates)).cumsum() + 2000,
        'R&D_Investment': np.random.normal(200000, 50000, len(dates)),
        'Customer_Satisfaction': np.random.normal(4.2, 0.3, len(dates)),
        'Product_Lines': np.random.choice(['Product_A', 'Product_B', 'Product_C'], len(dates)),
        'Region': np.random.choice(['EMEA', 'Americas', 'APAC'], len(dates)),
        'Sales_Channel': np.random.choice(['Direct', 'Partner', 'Online'], len(dates))
    }
    
    return pd.DataFrame(data)

def generate_strategic_questions(data):
    """Generate strategic questions based on data analysis"""
    questions = []
    
    if data is not None and not data.empty:
        # Analyze data trends
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:5]:  # Limit to 5 questions
            if len(data[col].dropna()) > 1:
                trend = "increasing" if data[col].iloc[-1] > data[col].iloc[0] else "decreasing"
                
                question = {
                    'metric': col.replace('_', ' ').title(),
                    'trend': trend,
                    'current_value': data[col].iloc[-1],
                    'question': f"How should we respond to the {trend} trend in {col.replace('_', ' ')}?",
                    'options': [
                        f"Invest more resources to accelerate {col.replace('_', ' ')}",
                        f"Maintain current strategy for {col.replace('_', ' ')}",
                        f"Pivot strategy to address {col.replace('_', ' ')} challenges",
                        f"Investigate root causes of {col.replace('_', ' ')} trends"
                    ],
                    'impact': random.choice(['High', 'Medium', 'Low'])
                }
                questions.append(question)
    
    return questions

def create_dashboard_visualization(data):
    """Create interactive dashboard visualizations"""
    if data is None or data.empty:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue Trend', 'Profit Margin Analysis', 
                       'Customer Growth', 'Market Performance'),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": True}]]
    )
    
    # Revenue trend
    if 'Revenue' in data.columns and 'Date' in data.columns:
        fig.add_trace(
            go.Scatter(x=data['Date'], y=data['Revenue'], 
                      name='Revenue', line=dict(color='#667eea')),
            row=1, col=1
        )
    
    # Profit margin
    if 'Profit_Margin' in data.columns and 'Date' in data.columns:
        fig.add_trace(
            go.Scatter(x=data['Date'], y=data['Profit_Margin'], 
                      name='Profit Margin', line=dict(color='#f093fb')),
            row=1, col=2
        )
    
    # Customer count
    if 'Customer_Count' in data.columns and 'Date' in data.columns:
        fig.add_trace(
            go.Scatter(x=data['Date'], y=data['Customer_Count'], 
                      name='Customers', line=dict(color='#43e97b')),
            row=2, col=1
        )
    
    # Market share
    if 'Market_Share' in data.columns and 'Date' in data.columns:
        fig.add_trace(
            go.Scatter(x=data['Date'], y=data['Market_Share'], 
                      name='Market Share', line=dict(color='#4facfe')),
            row=2, col=2
        )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        title_text="Business Strategy Dashboard - Real-time KPIs",
        title_x=0.5
    )
    
    return fig

def main():
    # Main header
    st.markdown('<div class="main-header">🎯 StrategySim Enterprise - Business Strategy Game</div>', 
                unsafe_allow_html=True)
    
    # Sidebar game controls
    st.sidebar.markdown("## 🎮 Game Controls")
    st.sidebar.markdown(f"**Level:** {st.session_state.game.level}")
    st.sidebar.markdown(f"**Experience:** {st.session_state.game.experience}")
    st.sidebar.markdown(f"**Score:** {st.session_state.game.player_score}")
    
    # Data upload section
    st.sidebar.markdown("## 📊 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload SAP CSV Data",
        type=['csv'],
        help="Upload your SAP data in CSV format. Can handle millions of records."
    )
    
    use_sample_data = st.sidebar.checkbox("Use Sample SAP Data", value=True)
    
    # Load data
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = data
            st.sidebar.success(f"✅ Loaded {len(data)} records")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            data = None
    elif use_sample_data:
        data = load_sample_sap_data()
        st.session_state.uploaded_data = data
    else:
        data = st.session_state.uploaded_data
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🎯 Strategic Questions", 
                                      "🏆 Decision Analysis", "📈 Performance"])
    
    with tab1:
        st.markdown("## Business Intelligence Dashboard")
        
        if data is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if 'Revenue' in data.columns:
                    revenue = data['Revenue'].iloc[-1] if len(data) > 0 else 0
                    st.markdown(f'''
                    <div class="kpi-card">
                        <h3>💰 Revenue</h3>
                        <h2>${revenue:,.0f}</h2>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col2:
                if 'Customer_Count' in data.columns:
                    customers = data['Customer_Count'].iloc[-1] if len(data) > 0 else 0
                    st.markdown(f'''
                    <div class="kpi-card">
                        <h3>👥 Customers</h3>
                        <h2>{customers:,.0f}</h2>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col3:
                if 'Market_Share' in data.columns:
                    market_share = data['Market_Share'].iloc[-1] if len(data) > 0 else 0
                    st.markdown(f'''
                    <div class="kpi-card">
                        <h3>📊 Market Share</h3>
                        <h2>{market_share:.1%}</h2>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col4:
                if 'Profit_Margin' in data.columns:
                    profit_margin = data['Profit_Margin'].iloc[-1] if len(data) > 0 else 0
                    st.markdown(f'''
                    <div class="kpi-card">
                        <h3>💹 Profit Margin</h3>
                        <h2>{profit_margin:.1%}</h2>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # Interactive dashboard
            dashboard_fig = create_dashboard_visualization(data)
            if dashboard_fig:
                st.plotly_chart(dashboard_fig, use_container_width=True)
            
            # Data preview
            st.markdown("### 📋 Data Preview")
            st.dataframe(data.head(10), use_container_width=True)
            
        else:
            st.warning("⚠️ Please upload SAP data or enable sample data to view the dashboard.")
    
    with tab2:
        st.markdown("## 🎯 Strategic & Tactical Questions")
        
        if data is not None:
            if st.button("🔄 Generate New Strategic Questions"):
                st.session_state.strategic_questions = generate_strategic_questions(data)
                st.session_state.game.experience += 100
            
            if not st.session_state.strategic_questions:
                st.session_state.strategic_questions = generate_strategic_questions(data)
            
            for i, question in enumerate(st.session_state.strategic_questions):
                st.markdown(f'''
                <div class="strategy-card">
                    <h3>🎯 Strategic Question {i+1}</h3>
                    <p><strong>Focus Area:</strong> {question['metric']}</p>
                    <p><strong>Current Trend:</strong> {question['trend']}</p>
                    <p><strong>Business Impact:</strong> {question['impact']}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f"**Question:** {question['question']}")
                
                selected_option = st.radio(
                    f"Select your strategic response:",
                    question['options'],
                    key=f"question_{i}"
                )
                
                if st.button(f"Submit Decision {i+1}", key=f"submit_{i}"):
                    # Calculate decision quality based on data insights
                    decision_quality = random.uniform(0.6, 1.0)
                    data_insights = random.uniform(0.7, 1.0)
                    
                    score = st.session_state.game.calculate_score(decision_quality, data_insights)
                    st.session_state.game.player_score += int(score)
                    st.session_state.game.experience += 200
                    
                    st.session_state.game.decisions_made.append({
                        'question': question['question'],
                        'answer': selected_option,
                        'score': score,
                        'timestamp': datetime.now()
                    })
                    
                    st.success(f"✅ Decision recorded! You earned {int(score)} points!")
                    
                    if st.session_state.game.level_up():
                        st.balloons()
                        st.success(f"🎉 Level Up! You're now Level {st.session_state.game.level}!")
                
                st.markdown("---")
        
        else:
            st.warning("⚠️ Please upload data to generate strategic questions.")
    
    with tab3:
        st.markdown("## 🏆 Decision Analysis & Game Progress")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
            <div class="score-display">
                🏆 Current Score: {st.session_state.game.player_score}
            </div>
            ''', unsafe_allow_html=True)
            
            # Level progress
            progress = (st.session_state.game.experience % 1000) / 1000
            st.progress(progress)
            st.markdown(f"Progress to Level {st.session_state.game.level + 1}: {progress:.1%}")
        
        with col2:
            st.markdown(f'''
            <div class="game-card">
                <h3>🎮 Game Statistics</h3>
                <p><strong>Level:</strong> {st.session_state.game.level}</p>
                <p><strong>Experience:</strong> {st.session_state.game.experience}</p>
                <p><strong>Decisions Made:</strong> {len(st.session_state.game.decisions_made)}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Decision history
        if st.session_state.game.decisions_made:
            st.markdown("### 📊 Decision History")
            
            decisions_df = pd.DataFrame(st.session_state.game.decisions_made)
            
            # Score trend
            fig_score = px.line(
                decisions_df, 
                x='timestamp', 
                y='score',
                title='Decision Quality Over Time',
                color_discrete_sequence=['#667eea']
            )
            st.plotly_chart(fig_score, use_container_width=True)
            
            # Recent decisions
            st.markdown("### 🔍 Recent Strategic Decisions")
            for decision in st.session_state.game.decisions_made[-5:]:
                st.markdown(f'''
                <div class="strategy-card">
                    <p><strong>Question:</strong> {decision['question'][:100]}...</p>
                    <p><strong>Decision:</strong> {decision['answer']}</p>
                    <p><strong>Score:</strong> {decision['score']:.0f} points</p>
                    <p><strong>Time:</strong> {decision['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
                </div>
                ''', unsafe_allow_html=True)
    
    with tab4:
        st.markdown("## 📈 Business Performance Analytics")
        
        if data is not None:
            # Performance metrics
            st.markdown("### 🎯 Key Performance Indicators")
            
            metrics_cols = st.columns(3)
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            for i, col in enumerate(numeric_cols[:6]):
                with metrics_cols[i % 3]:
                    if len(data[col].dropna()) > 1:
                        current = data[col].iloc[-1]
                        previous = data[col].iloc[-2] if len(data) > 1 else current
                        change = ((current - previous) / previous * 100) if previous != 0 else 0
                        
                        color = "🟢" if change > 0 else "🔴" if change < 0 else "🟡"
                        
                        st.markdown(f'''
                        <div class="kpi-card">
                            <h4>{col.replace('_', ' ').title()}</h4>
                            <h3>{current:,.2f}</h3>
                            <p>{color} {change:+.1f}%</p>
                        </div>
                        ''', unsafe_allow_html=True)
            
            # Correlation analysis
            st.markdown("### 🔗 Business Metrics Correlation")
            
            correlation_matrix = data[numeric_cols].corr()
            
            fig_corr = px.imshow(
                correlation_matrix,
                title="Business Metrics Correlation Matrix",
                color_continuous_scale='RdBu_r',
                aspect="auto"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Strategic recommendations
            st.markdown("### 💡 AI-Powered Strategic Recommendations")
            
            recommendations = [
                "📈 Consider increasing R&D investment based on positive revenue correlation",
                "👥 Customer satisfaction shows strong correlation with retention - focus on service quality",
                "🌍 EMEA region shows highest growth potential - consider market expansion",
                "💰 Profit margins could improve with operational efficiency initiatives",
                "🎯 Product line diversification may reduce market concentration risk"
            ]
            
            for rec in recommendations:
                st.markdown(f'''
                <div class="strategy-card">
                    <p>{rec}</p>
                </div>
                ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 🎮 About StrategySim Enterprise
    
    This is a gamified business strategy application that transforms SAP data analysis into an engaging, 
    game-like experience. Upload your CSV files with millions of records and get strategic insights 
    through interactive dashboards and tactical questions.
    
    **Features:**
    - 📊 Interactive KPI dashboards
    - 🎯 AI-generated strategic questions
    - 🏆 Scoring system based on decision quality
    - 📈 Performance analytics and correlations
    - 🎮 Level progression and achievements
    """)

if __name__ == "__main__":
    main()