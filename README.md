
---

# 🧠 Smart Support & Ticket Resolution System

### Intelligent AI-Powered Customer Support Automation

---

## 🚀 1. Project Overview

**Project Name:** Smart Support & Ticket Resolution System

A **Python Streamlit** web application that streamlines support ticket management with **AI-driven insights**.
The system automatically categorizes tickets, assigns agents, tracks resolution times, and provides real-time analytics dashboards.
It leverages **Groq + FAISS embeddings** for intelligent ticket resolution and knowledge retrieval.

### 🔑 Key Capabilities

* Submit and track customer support tickets.
* **AI-generated ticket resolutions** using RAG + LLM.
* Automatic categorization (category, priority, status).
* Dynamic agent assignment: *Sales, Marketing, Engineering, General Support.*
* Save and sync data with **Google Sheets**.
* Interactive analytics dashboard for ticket metrics and agent performance.

---

## 📋 2. Epics & Features

### **Epic 1: Ticket Submission**

**Features:**

* Capture customer, product, and issue details.
* Retrieve relevant context from FAISS vector store.
* Generate automated LLM-based resolution.
* Categorize and assign agent dynamically.
* Store ticket data in Google Sheets.

**Acceptance Criteria:**

* Ticket validation and storage successful.
* LLM-generated response is attached.
* Agent assignment aligns with ticket content.

---

### **Epic 2: Ticket Closure**

**Features:**

* Capture customer satisfaction rating (1–5).
* Auto-calculate resolution time.
* Update status to *Closed* and sync to Google Sheets.

**Acceptance Criteria:**

* Rating and closure timestamps recorded correctly.
* Closed tickets visible in analytics view.

---

### **Epic 3: Dashboard & Analytics**

**Features:**

* Metrics by ticket **Status**, **Priority**, **Channel**, and **Agent**.
* Visualizations via **Plotly**.

**Acceptance Criteria:**

* Charts display real-time metrics.
* Agent performance reflects accurate ticket counts.

---

## 🛠️ 3. Tasks / Implementation Steps

### **Frontend (Streamlit)**

* Ticket form with validation.
* AI-generated suggestions & auto-tagging.
* Ticket closure interface with satisfaction rating.
* Plotly-based visual dashboard.

### **Backend (Python + Google Sheets API)**

* Authentication & integration with Sheets API.
* CRUD operations for tickets.
* RAG (Retrieval-Augmented Generation) with FAISS.
* Agent assignment using Groq LLM.

### **Analytics (Plotly)**

* 📊 Ticket Status: *Open vs Closed*
* 📈 Ticket Priority: *Low, Medium, High, Critical*
* 🧩 Channels: *Web, Email, Phone*
* 👥 Agent Performance: *Sales, Marketing, Engineering, Support*

### **Testing / QA**

* Validate ticket workflow and AI responses.
* Verify Google Sheets synchronization.
* Cross-check dashboard metrics with stored data.

---

## 🧩 4. Architecture

**Frontend:** Streamlit
**Backend:** Python + Google Sheets API
**AI & RAG:** Groq LLM + FAISS embeddings
**Storage:** Google Sheets (`TicketDatabase`, Sheet2)
**Analytics:** Plotly (integrated in Streamlit UI)

### **Data Flow Diagram (Conceptual)**

```
Ticket Submission → FAISS KB Context → LLM Resolution  
      |                                   |
      v                                   v  
Categorize Ticket → Assign Agent → Save to Google Sheets  
      |  
      v  
Dashboard Metrics & Charts  
```

---

## 📁 5. Folder & File Structure

```
project/
├─ data/
│   ├─ customer_support_tickets.csv     # Raw ticket dataset
│   └─ terms.txt                        # Keyword and glossary data
│
├─ docs/
│   └─ agile_documentation.md           # Agile project documentation
│
├─ faiss_store/                         # FAISS vector store data
│
├─ .gitignore
├─ LICENSE
├─ requirements.txt                     # Python dependencies
│
├─ build_kb.py                          # Build knowledge base from terms/data
├─ dashboard.py                         # Streamlit dashboard UI
├─ g-sheets-int.py                      # Google Sheets integration
├─ upload_dataset.py                    # Upload and preprocess datasets
├─ processed_tickets.csv                # Processed or enriched ticket logs
├─ rag.py                               # AI (RAG + LLM) logic and agent assignment
├─ new.py                               # Utility or test module
└─ README.md                            # Project documentation (this file)
```

---

## 🧾 6. Key Data Points

| Field                                    | Description                      |
| ---------------------------------------- | -------------------------------- |
| `ticket_id`                              | Unique ticket identifier         |
| `customer_name`, `customer_email`        | Customer details                 |
| `product_purchased`, `date_of_purchase`  | Purchase metadata                |
| `ticket_subject`, `ticket_description`   | Issue details                    |
| `ticket_status`, `ticket_priority`       | Classification fields            |
| `ticket_channel`                         | Source (Web, Email, Phone, etc.) |
| `assigned_agent`                         | Agent assigned dynamically       |
| `first_response_time`, `resolution_time` | SLA metrics                      |
| `customer_satisfaction_rating`           | Feedback rating (1–5)            |

---

## 👥 Agents

* Sales
* Marketing
* Engineering
* General Support

---

## ⚙️ Ticket Classification

* **Priority:** Low / Medium / High / Critical
* **Status:** Open / Closed
* **Channel:** Web / Email / Phone / Other

---

## 📦 7. Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-support-system.git
cd smart-support-system

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run dashboard.py
```

---

## 🤖 8. Tech Stack

| Component     | Technology                                      |
| ------------- | ----------------------------------------------- |
| Frontend      | Streamlit                                       |
| Backend       | Python                                          |
| Database      | Google Sheets                                   |
| AI Model      | Groq LLM + Sentence Transformers (MiniLM-L6-v2) |
| Vector Store  | FAISS                                           |
| Visualization | Plotly                                          |
| Storage       | Google Sheets (TicketDatabase Sheet2)           |

---

## 🧠 9. Agile Documentation

See [docs/agile_documentation.md](./docs/agile_documentation.md).

---

## 🪪 License

This project is licensed under the terms of the [MIT License](./LICENSE).

---

