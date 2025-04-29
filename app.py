import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.exceptions import InconsistentVersionWarning
import warnings
import base64

# Function to add background from local file
# Load player statistics from CSV
player_stats_df = pd.read_csv('batting_stats_for_icc_mens_t20_world_cup_2024.csv')

# Check and print the column names to ensure the correct one is used
#st.write(player_stats_df.columns)

# Add some styling for better text visibility
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        file_extension = image_file.name.split('.')[-1].lower()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{file_extension};base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .main .block-container {{
                background-color: rgba(0, 0, 0, 0.5);  /* Darker background for better contrast */
                padding: 2rem;
                border-radius: 10px;
                color: white;  /* Set font color to white for better visibility */
            }}
            .input-label {{
                color: white;  /* Set input labels to white */
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: white;  /* Set all header colors to white */
            }}
            input {{
                color: white;  /* Set input text color to white */
                background-color: rgba(0, 0, 0, 0.5);  /* Match input background with the container */
            }}
            ::placeholder {{
                color: white;  /* Set placeholder text color to white */
            }}
            .stTextInput, .stTextArea, .stNumberInput {{
                color: white !important;
            }}
            .stButton {{
                color: white !important;
            }}
            .stWarning, .stSuccess, .stError {{
                color: white !important;
                background-color: rgba(0, 0, 0, 0.7) !important;  /* Darken the background of popup messages */
                border-radius: 5px !important;
                padding: 10px !important;
            }}
            /* Custom Styles for text shown in player stats and prediction */
            .stText {{
                color: white !important;
            }}
            .stSuccess, .stWarning, .stError, .stInfo {{
                color: white !important;  /* Set popup message text color to white */
                background-color: rgba(0, 0, 0, 0.7) !important;  /* Dark background */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error setting background: {str(e)}")

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
add_bg_from_local("cricket_bg.jpg")  # Ensure the image path is correct

# Load model
model = joblib.load('model (2).pkl')

# Session state to persist values across reruns
if 'Mat' not in st.session_state:
    st.session_state['Mat'] = 0
if 'Inns' not in st.session_state:
    st.session_state['Inns'] = 0
if 'NO' not in st.session_state:
    st.session_state['NO'] = 0
if 'Runs' not in st.session_state:
    st.session_state['Runs'] = 0
if 'SR' not in st.session_state:
    st.session_state['SR'] = 0
if 'Centuries' not in st.session_state:
    st.session_state['Centuries'] = 0
if 'Fifties' not in st.session_state:
    st.session_state['Fifties'] = 0
if 'Ducks' not in st.session_state:
    st.session_state['Ducks'] = 0

# Styling for the page
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64.b64encode(open("cricket_bg.jpg", "rb").read()).decode()}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }}
    h1, h2, h3, h4, h5, h6, label, .input-label {{
        color: white !important;
    }}
    input, .stTextInput > div > div > input {{
        color: white !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
    }}
    input::placeholder {{
        color: white !important;
    }}
    .stTextInput, .stTextArea, .stNumberInput {{
        color: white !important;
    }}
    .stButton {{
        color: white !important;
    }}
    .stWarning, .stSuccess, .stError, .stInfo {{
        color: white !important;
        background-color: rgba(0, 0, 0, 0.7) !important;  /* Darken the background of popup messages */
        border-radius: 5px !important;
        padding: 10px !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("Batting Performance Predictor")

# Input for player name
player_name = st.text_input("Enter Player Name", placeholder="Player Name", key="player_name").strip()

# Input for team name (Dropdown below player name)
teams = ["Afghanistan", "Australia", "Bangladesh", "Canada", "England", "India",
         "Ireland", "Namibia", "Nepal", "Netherlands", "New Zealand", "Oman",
         "Pakistan", "Papua New Guinea", "Scotland", "South Africa", "Sri Lanka",
         "Uganda", "United States of America", "West Indies"]
Team = st.selectbox("Select Team", teams)

if st.button("Get Player Statistics"):
    player_stats = player_stats_df[player_stats_df['Player'].str.contains(player_name, case=False, na=False)]
    
    if player_stats.empty:
        st.markdown("<p style='color:white;'>⚠️ No statistics found for the given player name.</p>", unsafe_allow_html=True)
    else:
        st.markdown(
    "<div style='background-color: rgba(0, 100, 0, 0.6); padding: 10px; border-radius: 5px; color: white;'>"
    "<strong>Player found!</strong> Populating statistics..."
    "</div>",
    unsafe_allow_html=True
)


        # Fill session_state from the first row of player_stats
        row = player_stats.iloc[0]
        
        # Ensure that columns exist and handle missing columns
        st.session_state['Mat'] = row.get('Mat', 0)
        st.session_state['Inns'] = row.get('Inns', 0)
        st.session_state['NO'] = row.get('NO', 0)
        st.session_state['Runs'] = row.get('Runs', 0)
        st.session_state['SR'] = row.get('SR', 0.0)
        st.session_state['Centuries'] = row.get('100', 0)
        st.session_state['Fifties'] = row.get('50s', 0)
        st.session_state['Ducks'] = row.get('0s', 0)

# Core stats input
st.header("Player Statistics")
Mat = st.number_input("Matches", min_value=0, key="Mat")
Inns = st.number_input("Innings", min_value=0, key="Inns")
NO = st.number_input("Not Outs", min_value=0, key="NO")
Runs = st.number_input("Runs", min_value=0, key="Runs")
SR = st.number_input("Strike Rate", min_value=0.0, key="SR", format="%.2f")
Centuries = st.number_input("100s", min_value=0, key="Centuries")
Fifties = st.number_input("50s", min_value=0, key="Fifties")
Ducks = st.number_input("0s", min_value=0, key="Ducks")

if st.button("Predict Performance"):
    try:
        # Input validation for matches and innings
        if Mat == 0 or Inns == 0:
            st.warning("Please enter valid match and innings data")
        else:
            # Calculate batting average
            calculated_avg = Runs / (Inns - NO) if (Inns - NO) > 0 else 0

            # Feature setup for prediction
            features = np.zeros(len(model.feature_names_in_))
            features[0] = Mat
            features[1] = Inns
            features[2] = NO
            features[3] = Runs
            features[4] = calculated_avg
            features[5] = SR
            features[6] = Centuries
            features[7] = Fifties
            features[8] = Ducks

            # Encode team feature
            team_feature = f"Team_{Team.replace(' ', '_')}"
            if team_feature in model.feature_names_in_:
                idx = np.where(model.feature_names_in_ == team_feature)[0][0]
                features[idx] = 1

            # Predict and show result
            prediction = model.predict([features])[0]
            if prediction < 0 or prediction > 200:
                st.markdown("<p style='color:white;'>⚠️ Prediction seems unrealistic. Please check inputs.</p>", unsafe_allow_html=True)
            else:
                st.markdown(
    f"<div style='background-color: rgba(0, 100, 0, 0.6); padding: 10px; border-radius: 5px; color: white;'>"
    f"<strong>Predicted Batting Average:</strong> {prediction:.2f}"
    "</div>",
    unsafe_allow_html=True
)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

