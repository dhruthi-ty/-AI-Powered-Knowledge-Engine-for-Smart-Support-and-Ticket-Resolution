import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from langchain_community.vectorstores import FAISS
from groq import Groq
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
import datetime

# ================================
# Load environment variables
# ================================
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
gemini_key = os.getenv("GOOGLE_API_KEY")

# ================================
# Google Sheets Setup
# ================================
SHEET_NAME = "TicketDatabase"
WORKSHEET = "Sheet2"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials/credentials.json", scope
)
gc = gspread.authorize(creds)
sheet = gc.open(SHEET_NAME).worksheet(WORKSHEET)

# ================================
# Static Keyword Mapping for fallback
# ================================
AGENT_MAPPING = {
    "Sales": ["pricing", "discount", "order", "invoice", "refund", "exchange"],
    "Marketing": ["promotion", "campaign", "ad", "social media"],
    "Engineering": ["bug", "error", "technical", "login", "feature"]
}

# ================================
# FAISS Vector Store Functions
# ================================
def load_vector_store():
    if not os.path.exists("faiss_store"):
        raise FileNotFoundError("❌ faiss_store not found. Run build_kb.py first.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_store", embeddings, allow_dangerous_deserialization=True)
    return vectorstore

def query_kb(query, vectorstore, top_k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([d.page_content for d in docs])
    return context

# ================================
# LLM Functions
# ================================
def ask_llm(query, context):
    client = Groq(api_key=groq_key)
    prompt = f"""
You are a helpful AI assistant for customer support.
Use the following context from the knowledge base to answer the question.

Context:
{context}

Question:
{query}

Answer in a concise and professional way:
"""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.4
    )
    return chat_completion.choices[0].message.content.strip()

def categorize_ticket(subject, description):
    client = Groq(api_key=groq_key)
    prompt = f"""
You are a customer support assistant.
Categorize the ticket based on subject and description.
Return a JSON with keys: category, priority, status.

Ticket Subject: {subject}
Ticket Description: {description}
"""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0
    )
    try:
        output = json.loads(response.choices[0].message.content)
        return output
    except:
        return {"category": "General", "priority": "Medium", "status": "Open"}

# ================================
# Agent Assignment
# ================================
def assign_agent(category, description, context=""):
    client = Groq(api_key=groq_key)
    prompt = f"""
You are an AI assistant for a customer support system.
Assign the ticket to the most suitable agent from this list ONLY:

- Sales
- Marketing
- Engineering
- General Support

Ticket Category: {category}
Ticket Description: {description}

Previous Customer Tickets (if any):
{context if context else 'None'}

Return ONLY one of these exact agent names as plain text.
"""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0
        )
        agent_name = response.choices[0].message.content.strip().lower()
        # Normalize LLM output
        mapping = {
            "sales": "Sales",
            "marketing": "Marketing",
            "engineering": "Engineering",
            "general support": "General Support"
        }
        agent_name = next((v for k, v in mapping.items() if k in agent_name), "General Support")
    except Exception:
        agent_name = "General Support"

    # Fallback keyword scoring
    text = f"{category} {description}".lower()
    scores = {agent: 0 for agent in AGENT_MAPPING}
    for agent, keywords in AGENT_MAPPING.items():
        for k in keywords:
            if k.lower() in text:
                scores[agent] += 1
    if max(scores.values()) > 0:
        agent_name = max(scores, key=scores.get)

    return agent_name

# ================================
# Google Sheets Headers
# ================================
HEADERS = [
    "ticket_id",
    "customer_name",
    "customer_email",
    "customer_age",
    "customer_gender",
    "product_purchased",
    "date_of_purchase",
    "ticket_type",
    "ticket_subject",
    "ticket_description",
    "ticket_status",
    "resolution",
    "ticket_priority",
    "ticket_channel",
    "first_response_time",
    "customer_satisfaction_rating",
    "assigned_agent"
]

# ================================
# Save or Update Ticket in Google Sheets
# ================================
def save_ticket_to_sheets(ticket):
    """
    Saves a ticket to Google Sheets. 
    Updates the row if ticket_id exists; otherwise appends a new row.
    """
    ticket_ids = sheet.col_values(1)  # Column A = ticket_id
    try:
        row_index = ticket_ids.index(ticket["ticket_id"]) + 1
        for col_index, header in enumerate(HEADERS, start=1):
            sheet.update_cell(row_index, col_index, ticket.get(header, ""))
    except ValueError:
        # Ticket ID not found → append new row
        row = [ticket.get(h, "") for h in HEADERS]
        sheet.append_row(row)

# ================================
# Process Ticket Pipeline
# ================================
def process_ticket(ticket, vectorstore):
    """
    Full ticket processing pipeline:
    1. Query KB for context
    2. Categorize ticket
    3. Assign agent
    4. Save to Google Sheets
    """
    kb_context = query_kb(ticket["ticket_description"], vectorstore)
    category_info = categorize_ticket(ticket["ticket_subject"], ticket["ticket_description"])
    
    ticket["category"] = category_info.get("category", "General")
    ticket["ticket_status"] = category_info.get("status", "Open")
    ticket["ticket_priority"] = category_info.get("priority", "Medium")
    
    ticket["assigned_agent"] = assign_agent(ticket["category"], ticket["ticket_description"], kb_context)
    
    # Set first_response_time if not already set
    if "first_response_time" not in ticket or not ticket["first_response_time"]:
        ticket["first_response_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    save_ticket_to_sheets(ticket)
    return ticket
