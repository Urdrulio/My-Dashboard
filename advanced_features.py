import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import random

class AdvancedBusinessAnalytics:
    """
    Advanced analytics engine for strategic business insights
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_importance = {}
        
    def predict_future_performance(self, data, target_column, periods=6):
        """
        Predict future business performance using machine learning
        """
        if data is None or len(data) < 10:
            return None
            
        # Prepare features
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        features = [col for col in numeric_cols if col != target_column]
        
        if len(features) < 2:
            return None
            
        X = data[features].fillna(data[features].mean())
        y = data[target_column].fillna(data[target_column].mean())
        
        # Train model
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        # Store feature importance
        self.feature_importance = dict(zip(features, self.model.feature_importances_))
        
        # Generate future predictions
        last_values = X.iloc[-1:].values
        predictions = []
        
        for i in range(periods):
            X_pred = self.scaler.transform(last_values)
            pred = self.model.predict(X_pred)[0]
            predictions.append(pred)
            
            # Update last values with some noise for next prediction
            last_values = last_values * (1 + np.random.normal(0, 0.02, last_values.shape))
        
        return predictions
    
    def analyze_risk_factors(self, data):
        """
        Analyze potential risk factors in business metrics
        """
        risks = []
        
        if data is None or data.empty:
            return risks
            
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if len(data[col].dropna()) > 3:
                # Calculate volatility
                volatility = data[col].std() / data[col].mean() if data[col].mean() != 0 else 0
                
                # Calculate trend
                if len(data[col]) > 1:
                    trend = (data[col].iloc[-1] - data[col].iloc[0]) / data[col].iloc[0] if data[col].iloc[0] != 0 else 0
                else:
                    trend = 0
                
                # Identify risks
                risk_level = "Low"
                risk_description = f"{col.replace('_', ' ')} shows stable performance"
                
                if volatility > 0.3:
                    risk_level = "High"
                    risk_description = f"High volatility detected in {col.replace('_', ' ')} ({volatility:.1%})"
                elif volatility > 0.15:
                    risk_level = "Medium"
                    risk_description = f"Moderate volatility in {col.replace('_', ' ')} ({volatility:.1%})"
                
                if trend < -0.1:
                    risk_level = "High"
                    risk_description = f"Declining trend in {col.replace('_', ' ')} ({trend:.1%})"
                elif trend < -0.05:
                    risk_level = "Medium" if risk_level == "Low" else risk_level
                    risk_description = f"Slight decline in {col.replace('_', ' ')} ({trend:.1%})"
                
                risks.append({
                    'metric': col.replace('_', ' ').title(),
                    'level': risk_level,
                    'description': risk_description,
                    'volatility': volatility,
                    'trend': trend
                })
        
        return sorted(risks, key=lambda x: {'High': 3, 'Medium': 2, 'Low': 1}[x['level']], reverse=True)
    
    def generate_strategic_scenarios(self, data):
        """
        Generate what-if scenarios for strategic planning
        """
        scenarios = []
        
        if data is None or data.empty:
            return scenarios
            
        scenarios = [
            {
                'name': 'Optimistic Growth',
                'description': 'Aggressive expansion with 20% increase in R&D and marketing',
                'changes': {
                    'R&D_Investment': 1.2,
                    'Marketing_Spend': 1.2,
                    'Expected_Revenue_Growth': 1.15
                },
                'probability': 0.3,
                'risk': 'Medium'
            },
            {
                'name': 'Conservative Growth',
                'description': 'Steady growth with focus on operational efficiency',
                'changes': {
                    'Operating_Costs': 0.95,
                    'Customer_Satisfaction': 1.05,
                    'Expected_Revenue_Growth': 1.08
                },
                'probability': 0.5,
                'risk': 'Low'
            },
            {
                'name': 'Market Disruption',
                'description': 'Defensive strategy against market disruption',
                'changes': {
                    'Market_Share': 0.9,
                    'Innovation_Investment': 1.3,
                    'Cost_Reduction': 0.85
                },
                'probability': 0.2,
                'risk': 'High'
            },
            {
                'name': 'Digital Transformation',
                'description': 'Major investment in digital capabilities',
                'changes': {
                    'Technology_Investment': 1.5,
                    'Process_Efficiency': 1.2,
                    'Customer_Experience': 1.25
                },
                'probability': 0.4,
                'risk': 'Medium'
            }
        ]
        
        return scenarios
    
    def calculate_kpi_health_score(self, data):
        """
        Calculate overall KPI health score
        """
        if data is None or data.empty:
            return 0
            
        scores = []
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if len(data[col].dropna()) > 1:
                # Trend score (positive trend = good)
                trend = (data[col].iloc[-1] - data[col].iloc[0]) / data[col].iloc[0] if data[col].iloc[0] != 0 else 0
                trend_score = min(max(trend * 10 + 5, 0), 10)  # Scale to 0-10
                
                # Stability score (low volatility = good)
                volatility = data[col].std() / data[col].mean() if data[col].mean() != 0 else 0
                stability_score = max(10 - volatility * 20, 0)
                
                # Combined score
                combined_score = (trend_score * 0.6 + stability_score * 0.4)
                scores.append(combined_score)
        
        return np.mean(scores) if scores else 5.0
    
    def generate_actionable_insights(self, data):
        """
        Generate actionable business insights
        """
        insights = []
        
        if data is None or data.empty:
            return insights
            
        # Correlation insights
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            
            # Find strong correlations
            for i, col1 in enumerate(numeric_cols):
                for j, col2 in enumerate(numeric_cols[i+1:], i+1):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        if corr_value > 0:
                            insights.append({
                                'type': 'Correlation',
                                'priority': 'High',
                                'insight': f"Strong positive correlation between {col1.replace('_', ' ')} and {col2.replace('_', ' ')} ({corr_value:.2f})",
                                'action': f"Leverage {col1.replace('_', ' ')} improvements to boost {col2.replace('_', ' ')}"
                            })
                        else:
                            insights.append({
                                'type': 'Correlation',
                                'priority': 'Medium',
                                'insight': f"Strong negative correlation between {col1.replace('_', ' ')} and {col2.replace('_', ' ')} ({corr_value:.2f})",
                                'action': f"Monitor {col1.replace('_', ' ')} to prevent negative impact on {col2.replace('_', ' ')}"
                            })
        
        # Performance insights
        for col in numeric_cols:
            if len(data[col].dropna()) > 3:
                recent_avg = data[col].tail(3).mean()
                historical_avg = data[col].head(-3).mean() if len(data) > 3 else recent_avg
                
                if recent_avg > historical_avg * 1.1:
                    insights.append({
                        'type': 'Performance',
                        'priority': 'High',
                        'insight': f"{col.replace('_', ' ')} has improved significantly ({((recent_avg/historical_avg-1)*100):.1f}%)",
                        'action': f"Identify and replicate success factors driving {col.replace('_', ' ')} improvement"
                    })
                elif recent_avg < historical_avg * 0.9:
                    insights.append({
                        'type': 'Performance',
                        'priority': 'High',
                        'insight': f"{col.replace('_', ' ')} has declined significantly ({((recent_avg/historical_avg-1)*100):.1f}%)",
                        'action': f"Immediate investigation required for {col.replace('_', ' ')} decline"
                    })
        
        return insights[:10]  # Return top 10 insights

class GameificationEngine:
    """
    Advanced gamification mechanics for business strategy game
    """
    
    def __init__(self):
        self.achievements = {
            'data_explorer': {
                'name': 'Data Explorer',
                'description': 'Upload your first dataset',
                'points': 100,
                'icon': '🔍'
            },
            'strategic_thinker': {
                'name': 'Strategic Thinker',
                'description': 'Answer 10 strategic questions',
                'points': 500,
                'icon': '🧠'
            },
            'decision_master': {
                'name': 'Decision Master',
                'description': 'Achieve 90%+ decision quality score',
                'points': 1000,
                'icon': '🎯'
            },
            'insight_generator': {
                'name': 'Insight Generator',
                'description': 'Generate 50 business insights',
                'points': 750,
                'icon': '💡'
            },
            'risk_manager': {
                'name': 'Risk Manager',
                'description': 'Identify high-risk scenarios',
                'points': 600,
                'icon': '🛡️'
            }
        }
        
    def check_achievements(self, game_state):
        """
        Check and award achievements based on game state
        """
        new_achievements = []
        
        # Data Explorer
        if 'data_explorer' not in game_state.achievements and hasattr(game_state, 'uploaded_data'):
            new_achievements.append('data_explorer')
        
        # Strategic Thinker
        if 'strategic_thinker' not in game_state.achievements and len(game_state.decisions_made) >= 10:
            new_achievements.append('strategic_thinker')
        
        # Decision Master (placeholder - would need actual quality calculation)
        if 'decision_master' not in game_state.achievements and len(game_state.decisions_made) >= 5:
            avg_score = np.mean([d['score'] for d in game_state.decisions_made]) if game_state.decisions_made else 0
            if avg_score >= 90:
                new_achievements.append('decision_master')
        
        return new_achievements
    
    def generate_challenges(self, data):
        """
        Generate dynamic challenges based on current data
        """
        challenges = []
        
        if data is None or data.empty:
            return challenges
            
        challenges = [
            {
                'title': '📈 Growth Accelerator',
                'description': 'Identify 3 metrics that could drive 15% revenue growth',
                'difficulty': 'Medium',
                'reward': 300,
                'deadline': datetime.now() + timedelta(days=7)
            },
            {
                'title': '🎯 Efficiency Expert',
                'description': 'Propose cost reduction strategies saving 10% operational costs',
                'difficulty': 'Hard',
                'reward': 500,
                'deadline': datetime.now() + timedelta(days=10)
            },
            {
                'title': '🔍 Risk Detective',
                'description': 'Identify and mitigate 2 high-risk business areas',
                'difficulty': 'Easy',
                'reward': 200,
                'deadline': datetime.now() + timedelta(days=5)
            },
            {
                'title': '💡 Innovation Champion',
                'description': 'Design a strategy to improve customer satisfaction by 20%',
                'difficulty': 'Hard',
                'reward': 600,
                'deadline': datetime.now() + timedelta(days=14)
            }
        ]
        
        return challenges
    
    def calculate_leaderboard_position(self, current_score, all_scores):
        """
        Calculate leaderboard position
        """
        if not all_scores:
            return 1
            
        sorted_scores = sorted(all_scores, reverse=True)
        try:
            position = sorted_scores.index(current_score) + 1
        except ValueError:
            position = len(sorted_scores) + 1
            
        return position

def create_advanced_visualization(data, viz_type):
    """
    Create advanced visualizations for strategic analysis
    """
    if data is None or data.empty:
        return None
        
    if viz_type == "forecast":
        # Revenue forecasting visualization
        analytics = AdvancedBusinessAnalytics()
        if 'Revenue' in data.columns:
            predictions = analytics.predict_future_performance(data, 'Revenue')
            
            if predictions:
                # Create forecast chart
                fig = go.Figure()
                
                # Historical data
                fig.add_trace(go.Scatter(
                    x=data['Date'] if 'Date' in data.columns else range(len(data)),
                    y=data['Revenue'],
                    mode='lines+markers',
                    name='Historical Revenue',
                    line=dict(color='#667eea')
                ))
                
                # Forecast data
                if 'Date' in data.columns:
                    last_date = pd.to_datetime(data['Date'].iloc[-1])
                    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=len(predictions), freq='M')
                else:
                    future_dates = range(len(data), len(data) + len(predictions))
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=predictions,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='#f093fb', dash='dash')
                ))
                
                fig.update_layout(
                    title='Revenue Forecast - Next 6 Periods',
                    xaxis_title='Time Period',
                    yaxis_title='Revenue',
                    height=400
                )
                
                return fig
    
    elif viz_type == "risk_analysis":
        # Risk analysis heatmap
        analytics = AdvancedBusinessAnalytics()
        risks = analytics.analyze_risk_factors(data)
        
        if risks:
            risk_df = pd.DataFrame(risks)
            
            # Create risk matrix
            fig = px.scatter(
                risk_df,
                x='volatility',
                y='trend',
                size=[10] * len(risk_df),
                color='level',
                hover_data=['metric', 'description'],
                title='Risk Analysis Matrix',
                color_discrete_map={'High': '#ff4757', 'Medium': '#ffa502', 'Low': '#2ed573'}
            )
            
            fig.update_layout(
                xaxis_title='Volatility',
                yaxis_title='Trend',
                height=400
            )
            
            return fig
    
    elif viz_type == "correlation_network":
        # Correlation network visualization
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 2:
            corr_matrix = data[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                title='Business Metrics Correlation Network',
                color_continuous_scale='RdBu_r',
                aspect="auto"
            )
            
            return fig
    
    return None