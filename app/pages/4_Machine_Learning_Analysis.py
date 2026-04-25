from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
import streamlit as st
import plotly.express as px
import pandas as pd 
import joblib 
from pathlib import Path
from src.common.setup_directories import FEATURES_DIR, MODELS_DIR
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))


@st.cache_resource
def load_models():
    # Load models and model dataset
    driver_model = joblib.load(MODELS_DIR / 'finish_position_model.pkl')
    team_model = joblib.load(MODELS_DIR / 'team_consistency_model.pkl')
    
    return driver_model, team_model
    
@st.cache_data
def load_data():
    model_df = pd.read_csv(FEATURES_DIR / 'model_dataset.csv')
    team_info_df = pd.read_csv(FEATURES_DIR / 'team_features.csv').drop_duplicates(subset=['Abbreviation'])
    team_info_df = team_info_df[['Abbreviation', 'TeamName']]
    
    driver_rows = len(pd.read_csv(FEATURES_DIR / 'driver_features.csv'))
    team_rows = len(pd.read_csv(FEATURES_DIR / 'team_features.csv'))
    race_rows = len(pd.read_csv(FEATURES_DIR / 'race_features.csv'))
    model_rows = len(model_df)

    return model_df, team_info_df, driver_rows, team_rows, race_rows, model_rows

TEAM_COLORS = {
    "Mercedes": "#00D7B6",
    "Red Bull": "#4781D7",
    "Ferrari": "#ED1131",
    "McLaren": "#F47600",
    "Alpine": "#00A1E8",
    "Racing Bulls": "#6C98FF",
    "Aston Martin": "#229971",
    "Williams": "#1868DB",
    "Kick Sauber": "#01C00E",
    "Haas": "#9C9FA2",
}

driver_model, team_model = load_models()
model_df, team_info_df, driver_rows, team_rows, race_rows, model_rows = load_data()

# One-hot encode SafetyCar, VirtualSafetyCar, RedFlag
model_df[['SafetyCar', 'VirtualSafetyCar', 'RedFlag']] = model_df[['SafetyCar', 'VirtualSafetyCar', 'RedFlag']].astype(int)

# Prepare driver & team features
driver_features = model_df.drop(columns=['Abbreviation', 'Year', 'RoundNumber', 'Event', 'Position', 'AvgTeamFinishLast3', 'AvgTeamFinishLast5', 'TeamDNFRate', 'AvgTeamPitTime', 'AvgTeamPitTimeLast3', 'AvgTeamPitTimeLast5'])
team_features = model_df[['AvgTeamFinishLast3', 'TeamDNFRate', 'Corners', 'TrackLength', 'TotalLaps', 'TrackTemp', 'AirTemp', 'Rainfall', 'SafetyCar', 'VirtualSafetyCar', 'RedFlag']]
 
y = model_df['Position']

driver_pred = driver_model.predict(driver_features)
team_pred = team_model.predict(team_features)

mae = mean_absolute_error(y, driver_pred)
rmse = root_mean_squared_error(y, driver_pred)
r2 = r2_score(y, driver_pred)

st.title('ML Model Performance')
st.caption('Trained on 2023-2024 data (894 rows)')

# ML Model Performance
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4, border=True)
    col1.metric('Model', 'Random Forest')
    col2.metric('MAE', round(mae, 2))
    col3.metric('RMSE', round(rmse, 2))
    col4.metric('R2', round(r2, 2))

# Feature importance charts
driver_feature_importance = pd.DataFrame({
    'Feature': driver_features.columns,
    'Importance': driver_model.feature_importances_
}).sort_values('Importance', ascending=True).tail(10)

team_feature_importance = pd.DataFrame({
    'Feature': team_features.columns,
    'Importance': team_model.feature_importances_
}).sort_values('Importance', ascending=True).tail(10)

plot1, plot2 = st.columns(2)

with plot1:
    with st.container(border=True):
        fig1 = px.bar(driver_feature_importance,
                    x='Importance',
                    y='Feature',
                    title='Driver Feature Importance',
                    orientation='h')
        st.plotly_chart(fig1)
with plot2:
    with st.container(border=True):
        fig2 = px.bar(team_feature_importance, 
                    x='Importance', 
                    y='Feature', 
                    title='Team Feature Importance',
                    orientation='h',
                    color_discrete_sequence=['#ED1131'])
        st.plotly_chart(fig2)
with st.expander("Feature Importance Analysis"):
    st.write("""The driver model identifies qualifying-related features (GridPosition, QualiDelta) and 
             recent finishing form (AvgFinishLast3, AvgFinishLast5) as the strongest predictors of race 
             outcome. This aligns with F1 intuition — where you start on the grid heavily constrains where 
             you can finish, and a driver's recent results reflect their current car performance and confidence. 
             Average lap time features also rank highly, capturing raw pace that doesn't always show up in 
             final positions due to strategy or incidents. The team model places the most weight on 
             AvgTeamFinishLast3 and TeamDNFRate, reflecting that team-level reliability and recent constructor 
             form are the clearest signals of mechanical competitiveness independent of individual driver skill.""")

# Predicted vs Actual Scatterplot 
plot3, plot4, plot5 = st.columns(3)

plot_df = pd.DataFrame({
    'Actual': y,
    'Predicted': driver_pred,
    'Abbreviation': model_df['Abbreviation']
})
plot_df = plot_df.merge(team_info_df, on='Abbreviation', how='left')

with plot3:
    with st.container(border=True):
        fig3 = px.scatter(plot_df,
                  x='Actual',
                  y='Predicted',
                  title='Predicted vs Actual Finishing Position',
                  hover_data=['Abbreviation'],
                  opacity=0.5)
        fig3.add_shape(type='line', x0=1, y0=1, x1=20, y1=20,
               line=dict(color='white', dash='dash'))
        fig3.add_annotation(x=18, y=2,
                    text=f'R² = {round(r2, 2)}',
                    showarrow=False,
                    font=dict(color='white', size=13))
        st.plotly_chart(fig3)
    
        
# Residual Distribution Graph
plot_df['Residual'] = plot_df['Predicted'] - plot_df['Actual']

with plot4:
    with st.container(border=True):
        fig4 = px.histogram(plot_df,
                            x='Residual',
                            title='Prediction Residuals',
                            nbins=30,
                            color_discrete_sequence=['#ED1131'])
        fig4.add_vline(x=0, line_dash='dash', line_color='white')
        st.plotly_chart(fig4)
with st.expander("Model Performance Analysis"):
    st.write("""An R² of 0.68 means the model explains approximately 68% of the variance in finishing positions 
             across the 2023–2024 seasons — a meaningful result given how much randomness exists in F1 racing. 
             Safety cars, first-lap incidents, strategy calls, and mechanical failures introduce noise that no 
             statistical model can fully anticipate. The predicted vs actual scatter shows the model performs 
             most accurately for front-running positions (1–8), where car performance dominates outcomes. 
             Spread increases toward the midfield and back of the grid, where results are more volatile. 
             The residual distribution being centered near zero confirms the model has no systematic bias — 
             it does not consistently over or under predict finishing positions — with the slight tail 
             representing genuine outlier races where unexpected events determined the result.""")
        
data_overview_df = pd.DataFrame({
    'File': ['driver_features.csv', 'team_features.csv', 'race_features.csv', 'model_dataset.csv'],
    'Rows': [driver_rows, team_rows, race_rows, model_rows]
})  
with plot5:
    with st.container(border=True):
        st.subheader('Data Overview')
        st.dataframe(data_overview_df, hide_index=True)