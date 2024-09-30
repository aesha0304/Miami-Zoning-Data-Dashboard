###Miami-Zoning-Data-Dashboard
This project processes and visualizes Miami zoning data from public meetings. It extracts important information such as meeting dates, chairperson details, zoning requests, and vote outcomes from JSON data, converts it into CSV format, and provides interactive visualizations using Dash and Plotly.

Features
Data Extraction: Extracts meeting details from a JSON file and cleans it for further processing.
CSV Conversion: Converts the processed data into CSV format.
Data Visualization: Provides interactive graphs and charts, including:
Zoning decisions over time
Approval status distribution
Chairperson vote counts
Interactive Dashboard: Allows users to filter data by approval status and date range, updating the visualizations and data table dynamically.
Project Workflow
Data Extraction (hack.py):

Reads Miami zoning data from a JSON file.
Cleans and extracts key information such as meeting date, time, location, and zoning requests.
Outputs the cleaned data to a CSV file for further analysis.
Data Visualization Dashboard (hack2.py):

Loads the CSV data into a Pandas DataFrame.
Uses Plotly Dash to create interactive visualizations, allowing users to explore zoning decisions, vote outcomes, and approval status.
Installation
Clone the repository:

git clone https://github.com/your-username/miami-zoning-dashboard.git
cd miami-zoning-dashboard
Install the required dependencies:

pip install -r requirements.txt
Run the dashboard:

python hack2.py
Usage
Run Data Extraction: First, ensure that you have the correct path for the input JSON file in hack.py. Then, run the script to extract the zoning data and generate a CSV file:

python hack.py
Launch the Dashboard: Once the CSV file is ready, run the Dash app (hack2.py) to visualize the data:
python hack2.py
Filter Data: Use the dashboard to filter the data by date range or approval status. The graphs and tables will automatically update based on your selections.

Requirements
Python 3.x
Dash
Plotly
Pandas
JSON and CSV libraries
Project Files
hack.py: Script for extracting and cleaning data from JSON files, saving results to CSV.
hack2.py: Dash app that provides interactive visualizations and filters for exploring the zoning data.
Future Enhancements
Geospatial Data: Add maps to visualize zoning decisions geographically.
Additional Filters: Implement more filtering options, such as zoning type or specific commissioners.
Real-Time Data Updates: Enable real-time updates as new zoning data becomes available.
License
This project is licensed under the MIT License - see the LICENSE file for details.
