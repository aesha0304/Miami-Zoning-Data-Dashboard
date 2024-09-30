import json
import csv
import re

# Load the JSON file
json_file_path = 'C:/Users/aesha/hackathon/miami_data.json'
csv_file_path = 'C:/Users/aesha/hackathon/cl_miami_zoning_data.csv'

# Open and load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Define the headers for the CSV
headers = ['Meeting Date', 'Meeting Time', 'Location', 'Chairperson', 'Vice Chairperson', 
           'Commissioners Present', 'Commissioners Absent', 'Commissioners Late', 
           'Invocation By', 'Invocation Requests', 'Zoning Item Number', 'Zoning Item Title', 
           'Zoning Request', 'Zoning Item Location', 'Zoning Vote Result', 'Mover', 
           'Seconder', 'Vote Count', 'Absent During Vote']

# Function to clean up and extract details from the JSON text
def extract_field(pattern, text, default="Unknown"):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    # Loop through each meeting entry in the JSON data
    for meeting_date, meeting_info in data.items():
        # Extract meeting time (assuming it's usually at 9:30 AM)
        meeting_time = extract_field(r'(\d{1,2}:\d{2}:\d{2}\s*[AP]M)', meeting_info, '9:30:00 AM')
        
        # Extract location
        location = extract_field(r'Commission Chambers\s*([^,]+)', meeting_info, "Commission Chambers")
        
        # Extract chairperson and vice chairperson
        chairperson = extract_field(r'Chairman,?\s*([A-Za-z\s.]+)', meeting_info, "Unknown")
        vice_chairperson = extract_field(r'Vice Chairwoman,?\s*([A-Za-z\s.]+)', meeting_info, "Unknown")
        
        # Extract commissioners present, absent, and late
        commissioners_present = extract_field(r'Members Present:\s*([^;]+)', meeting_info, "Unknown")
        commissioners_absent = extract_field(r'Members Absent:\s*([^;]+)', meeting_info, "Unknown")
        commissioners_late = extract_field(r'Members Late:\s*([^;]+)', meeting_info, "None")
        
        # Invocation details
        invocation_by = extract_field(r'Sergeant-at-Arms\s*([^,]+)', meeting_info, "Unknown")
        invocation_requests = extract_field(r'remembered in the invocation\s*([^;]+)', meeting_info, "None")
        
        # Zoning item details
        zoning_item_number = extract_field(r'Zoning HEARING NO.\s*(\d+-\d+)', meeting_info, "Unknown")
        zoning_item_title = extract_field(r'Zoning HEARING NO.\s*\d+-\d+\s*--\s*(DISTRICT\S?\s*\d+)\s*--\s*([^,]+)', meeting_info, "Unknown")
        zoning_request = extract_field(r'REQUEST\(S\):\s*([^.]+)', meeting_info, "Unknown")
        zoning_item_location = extract_field(r'LOCATION:\s*([^\n]+)', meeting_info, "Unknown")
        zoning_vote_result = "Approved" if "Approved" in meeting_info else "Unknown"
        
        # Vote details
        mover = extract_field(r'Mover:\s*([A-Za-z\s.]+)', meeting_info, "Unknown")
        seconder = extract_field(r'Seconder:\s*([A-Za-z\s.]+)', meeting_info, "Unknown")
        vote_count = extract_field(r'Vote:\s*(\d+\s*-\s*\d+)', meeting_info, "Unknown")
        absent_during_vote = extract_field(r'Absent:\s*([^\n]+)', meeting_info, "Unknown")

        # Write the row to the CSV file
        row = {
            'Meeting Date': meeting_date,
            'Meeting Time': meeting_time,
            'Location': location,
            'Chairperson': chairperson,
            'Vice Chairperson': vice_chairperson,
            'Commissioners Present': commissioners_present,
            'Commissioners Absent': commissioners_absent,
            'Commissioners Late': commissioners_late,
            'Invocation By': invocation_by,
            'Invocation Requests': invocation_requests,
            'Zoning Item Number': zoning_item_number,
            'Zoning Item Title': zoning_item_title,
            'Zoning Request': zoning_request,
            'Zoning Item Location': zoning_item_location,
            'Zoning Vote Result': zoning_vote_result,
            'Mover': mover,
            'Seconder': seconder,
            'Vote Count': vote_count,
            'Absent During Vote': absent_during_vote
        }
        
        writer.writerow(row)

print(f"CSV file has been created at {csv_file_path}")
