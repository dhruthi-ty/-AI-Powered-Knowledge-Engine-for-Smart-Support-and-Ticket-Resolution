Smart Support & Ticket Resolution System – Agile Documentation
1. Project Overview

Project Name: Smart Support & Ticket Resolution System
Description:
A Python Streamlit web application for managing support tickets. It automatically categorizes tickets, assigns them to agents, tracks resolution times, and provides analytics dashboards. AI (Groq + FAISS embeddings) is used for intelligent ticket processing and knowledge retrieval.

Key Capabilities:

Submit tickets with customer and product details.

AI-generated ticket resolution suggestions using RAG + LLM.

Categorization of tickets (category, priority, status).

Dynamic agent assignment (Sales, Marketing, Engineering, General Support).

Save and update tickets in Google Sheets.

Analytics dashboard: ticket status, priority, channel, and agent performance.

2. Epics & Features
Epic 1: Ticket Submission

Features:

Capture ticket details: customer info, product info, subject, description.

AI retrieval from vector store for relevant knowledge.

Generate automated resolution using LLM.

Categorize ticket into category, priority, and status.

Assign ticket to an appropriate agent.

Save ticket in Google Sheets with first response timestamp.

Acceptance Criteria:

Ticket data is validated and stored correctly.

LLM resolution is generated and saved.

Agent assignment is accurate based on category and description.

Epic 2: Ticket Closure

Features:

Record customer satisfaction rating (1–5).

Calculate ticket resolution time automatically.

Update ticket status to Closed.

Save updates in Google Sheets.

Acceptance Criteria:

Rating and resolution time are recorded accurately.

Closed tickets reflect properly in storage.

Epic 3: Dashboard & Analytics

Features:

Ticket Status Metrics: Only Open vs Closed.

Ticket Priority Metrics: Low, Medium, High, Critical.

Ticket Channels Metrics: Web, Email, Phone, and up to 5 channels.

Agent Performance Metrics: Only for Sales, Marketing, Engineering, General Support.

Acceptance Criteria:

Dashboard shows accurate counts for tickets by status, priority, and channel.

Agent performance charts display tickets assigned correctly.

3. Tasks / Implementation Steps

Frontend (Streamlit):
Ticket submission form and validation.
Display AI-generated resolution and automatic tags.
Ticket closure and rating interface.
Dashboard charts (Plotly) for tickets and agents.
Backend (Python + Google Sheets API):
Connect and authenticate to Google Sheets.
Store and update ticket data.
Retrieve historical tickets for context.
Integrate RAG vector store (FAISS) for knowledge retrieval.
Categorize tickets and assign agents using Groq LLM.

Analytics (Plotly):
Pie chart: Ticket Status (Open vs Closed).
Bar chart: Ticket Priority (Low, Medium, High, Critical).
Pie chart: Ticket Channel (Web, Email, Phone, etc.).
Bar chart: Agent Performance (assigned tickets only for Sales, Marketing, Engineering, General Support).

Testing / QA:
Verify ticket submission workflow.
Test AI-generated resolutions and categorization.
Ensure agent assignment aligns with category and keywords.
Validate dashboard metrics against Google Sheets data.

4. Architecture

Frontend: Streamlit
Backend: Python + Google Sheets API
AI & RAG Integration: Groq LLM + FAISS embeddings (sentence-transformers/all-MiniLM-L6-v2)
Storage: Google Sheets (Sheet2 of TicketDatabase)
Analytics: Plotly charts embedded in Streamlit

Data Flow Diagram (Conceptual):

Ticket Submission --> FAISS KB Context --> LLM Resolution
      |                                      |
      v                                      v
Categorize Ticket --> Assign Agent --> Save/Update in Google Sheets
      |
      v
Dashboard Metrics & Charts

5. Folder & File Structure
project/
├─ app.py                     # Main Streamlit app
├─ rag.py                     # AI, ticket processing, agent assignment
├─ credentials/               # Google Sheets credentials
│   └─ credentials.json
├─ faiss_store/               # FAISS vector store data
├─ requirements.txt           # Python dependencies
├─ .env                       # API keys (GROQ, Google)
└─ docs/
    └─ agile_documentation.md # This Agile documentation

6. Key Data Points

Ticket Fields: ticket_id, customer_name, customer_email, product_purchased, date_of_purchase, ticket_subject, ticket_description, ticket_status, ticket_priority, ticket_channel, assigned_agent, first_response_time, customer_satisfaction_rating.

Agents: Sales, Marketing, Engineering, General Support.

Ticket Priority: Low, Medium, High, Critical.

Ticket Status: Open, Closed.

Channels: Web, Email, Phone, etc.