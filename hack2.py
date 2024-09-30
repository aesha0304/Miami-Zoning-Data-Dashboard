import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import google.generativeai as genai
import os
import time
import plotly.express as px

# Setup the Google Gemini API
genai.configure(api_key="AIzaSyCHnpYkvoP7FJYGSWLo_1BZ7f8_EY9dUr8")

# Function to upload file to Gemini
def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

# Load and preprocess the CSV file
csv_file_path = 'cleaned_miami_board_meetings.csv'
df = pd.read_csv(csv_file_path)
df['Date'] = pd.to_datetime(df['Date'])

# Upload the file to Gemini and ensure it's active
files = [upload_to_gemini(csv_file_path, mime_type="text/csv")]
wait_for_files_active(files)

# Create a chatbot session with the Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                files[0],
                "use this file to answer any questions about Miami Zoning Board meetings data."
            ],
        },
    ]
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div(children=[
    html.H1(children='Miami Zoning Board Meetings Dashboard', style={'text-align': 'center'}),
    
    # AI Assistant Section
    html.Div([
        html.Label('Ask the AI Assistant:'),
        dcc.Input(id='user-input', type='text', placeholder='Ask something...', style={'width': '80%'}),
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Div(id='chatbot-response', style={'margin-top': '10px'})
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),

    # Dropdown for filtering by approval status
    html.Div([
        html.Label('Filter by Approval Status:'),
        dcc.Dropdown(
            id='approval-status-filter',
            options=[{'label': status, 'value': status} for status in df['Approval Status'].unique()] + [{'label': 'All', 'value': 'All'}],
            value='All',  # Default value
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
    
    # Date picker range for selecting date range
    html.Div([
        html.Label('Select Date Range:'),
        dcc.DatePickerRange(
            id='date-range-picker',
            min_date_allowed=min(df['Date']),
            max_date_allowed=max(df['Date']),
            start_date=min(df['Date']),
            end_date=max(df['Date'])
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
    
    # Graphs
    dcc.Graph(id='zoning-decisions-graph'),
    dcc.Graph(id='approval-distribution-pie'),
    dcc.Graph(id='chairperson-vote-bar'),

    # Data Table
    html.Div([
        dash_table.DataTable(
            id='filtered-data-table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=[],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
        )
    ], style={'padding': '20px'})
])

# Callback to handle chatbot responses using the Gemini API
@app.callback(
    Output('chatbot-response', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('user-input', 'value')]
)
def generate_response(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        try:
            response = chat_session.send_message(user_input)
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    return "Ask me anything about Miami Zoning Board meetings!"

# Callback to update graphs and data table based on filters
@app.callback(
    [Output('zoning-decisions-graph', 'figure'),
     Output('approval-distribution-pie', 'figure'),
     Output('chairperson-vote-bar', 'figure'),
     Output('filtered-data-table', 'data')],
    [Input('approval-status-filter', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_graphs(selected_status, start_date, end_date):
    # Filter the data based on user selections
    filtered_df = df.copy()

    # Filter by date range
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    # Filter by approval status
    if 'All' not in selected_status:
        filtered_df = filtered_df[filtered_df['Approval Status'].isin(selected_status)]

    # Create the zoning decisions graph (over time)
    zoning_decisions_fig = px.histogram(
        filtered_df,
        x='Date',
        color='Approval Status',
        title='Zoning Decisions Over Time',
        labels={'Approval Status': 'Approval Status'}
    )

    # Create a pie chart for approval status distribution
    approval_pie_fig = px.pie(
        filtered_df,
        names='Approval Status',
        title='Approval Status Distribution',
        hole=.3
    )

    # Create a bar chart for votes by chairperson
    chairperson_vote_bar_fig = px.bar(
        filtered_df,
        x='Chairperson',
        y='Vote',
        color='Approval Status',
        title='Votes by Chairperson',
        labels={'Chairperson': 'Chairperson Name', 'Vote': 'Vote Count'}
    )

    # Update the data table
    table_data = filtered_df.to_dict('records')

    return zoning_decisions_fig, approval_pie_fig, chairperson_vote_bar_fig, table_data

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
