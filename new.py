import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

# Authorize client
client = gspread.authorize(creds)

# Open the sheet by name
sheet = client.open("MyDatabaseSheet").sheet1  # first worksheet

# Read all records into a list of dicts
data = sheet.get_all_records()

# Convert to pandas DataFrame
df = pd.DataFrame(data)

print(df.head())


# Update a single cell
sheet.update_cell(2, 3, "Hello World")  # row=2, col=3

# Append a row
sheet.append_row(["2025-08-25", "John Doe", 100])
