import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import math
import time

# ================================
# STEP 1: Connect to Google Sheets
# ================================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials/credentials.json", scope
)
client = gspread.authorize(creds)

SHEET_NAME = "TicketDatabase"
sheet = client.open(SHEET_NAME).sheet1

# ================================
# STEP 2: Load & Preprocess Dataset
# ================================
df = pd.read_csv("data/customer_support_tickets.csv")

# Enforce fixed taxonomy
taxonomy = [
    "ticket_id", "customer_name", "customer_email", "customer_age", "customer_gender",
    "product_purchased", "date_of_purchase", "ticket_type", "ticket_subject",
    "ticket_description", "ticket_status", "resolution", "ticket_priority",
    "ticket_channel", "first_response_time",
    "customer_satisfaction_rating", "assigned_agent"
]

# Ensure all taxonomy columns exist in DataFrame
for col in taxonomy:
    if col not in df.columns:
        df[col] = ""

df = df[taxonomy]  # reorder

# Clean NaN
df = df.fillna("").astype(str)

# ================================
# STEP 3: Upload to Google Sheets
# ================================
print("Uploading to Google Sheet...")

sheet.clear()
sheet.resize(rows=len(df) + 1, cols=len(df.columns))

headers = df.columns.tolist()
sheet.update(values=[headers], range_name="A1")

batch_size = 200
num_batches = math.ceil(len(df) / batch_size)

for i in range(num_batches):
    start = i * batch_size
    end = min((i + 1) * batch_size, len(df))
    batch = df.iloc[start:end].values.tolist()

    print(f"Uploading batch {i+1}/{num_batches} (rows {start+1}-{end})...")

    sheet.update(
        values=batch,
        range_name=f"A{start+2}"
    )
    time.sleep(2)

print("✅ All rows uploaded successfully to Google Sheets")
