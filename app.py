# app.py
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from rag import (
    load_vector_store, query_kb, ask_llm, 
    categorize_ticket, save_ticket_to_sheets, assign_agent, sheet
)

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="Smart Support Ticket System", layout="wide")
st.title("📩 Smart Support & Ticket Resolution System")

# Load vector store
vectorstore = load_vector_store()

# -------------------------------
# Sidebar Menu
# -------------------------------
menu = st.sidebar.selectbox("Menu", ["Submit Ticket", "Dashboard"])

# ===============================
# Submit Ticket Page
# ===============================
if menu == "Submit Ticket":
    st.subheader("Enter Ticket Details")

    with st.form("ticket_form"):
        customer_name = st.text_input("Customer Name")
        customer_email = st.text_input("Customer Email")
        customer_age = st.text_input("Customer Age")
        customer_gender = st.selectbox("Customer Gender", ["Male", "Female", "Other"])
        product_purchased = st.text_input("Product Purchased")
        date_of_purchase = st.date_input("Date of Purchase", datetime.date.today())
        
        ticket_subject = st.text_input("Ticket Subject")
        ticket_description = st.text_area("Ticket Description")
        
        submit_button = st.form_submit_button(label="Submit Ticket")

    if submit_button:
        ticket_id = f"TK-{int(datetime.datetime.now().timestamp())}"

        # Step 1: Retrieve RAG context
        kb_context = query_kb(ticket_description, vectorstore)

        # Step 2: Include previous tickets of same user
        historical_data = sheet.get_all_records()
        historical_tickets = pd.DataFrame(historical_data)
        history_context = ""
        if not historical_tickets.empty:
            customer_history = historical_tickets[historical_tickets['customer_email'] == customer_email]
            if not customer_history.empty:
                history_context = "\n".join([
                    f"Subject: {row['ticket_subject']}, Description: {row['ticket_description']}, Status: {row['ticket_status']}"
                    for _, row in customer_history.iterrows()
                ])

        # Step 3: Combine KB + history
        full_context = f"{kb_context}\n\nPrevious Tickets:\n{history_context}" if history_context else kb_context

        # Step 4: Generate LLM resolution
        resolution = ask_llm(ticket_description, full_context)

        # Step 5: Categorize ticket
        cat_info = categorize_ticket(ticket_subject, ticket_description)

        # Step 6: Assign agent
        agent = assign_agent(cat_info["category"], ticket_description, context=full_context)

        # Step 7: Prepare ticket data
        first_response_time = datetime.datetime.now()
        ticket_data = {
            "ticket_id": ticket_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_age": customer_age,
            "customer_gender": customer_gender,
            "product_purchased": product_purchased,
            "date_of_purchase": date_of_purchase.strftime("%Y-%m-%d"),
            "ticket_type": "Support",
            "ticket_subject": ticket_subject,
            "ticket_description": ticket_description,
            "ticket_status": cat_info["status"],
            "resolution": resolution,
            "ticket_priority": cat_info["priority"],
            "ticket_channel": "Web",
            "first_response_time": first_response_time.strftime("%Y-%m-%d %H:%M:%S"),
            "customer_satisfaction_rating": "",
            "assigned_agent": agent,
            "time_to_resolution": ""
        }

        # Step 8: Save to Google Sheets
        save_ticket_to_sheets(ticket_data)
        st.session_state.latest_ticket = ticket_data

        # Step 9: Display results
        st.success("✅ Ticket submitted successfully!")
        st.subheader("📌 Generated Response")
        st.write(resolution)
        st.subheader("📝 Automatic Tags")
        st.write(f"Category: {cat_info['category']}")
        st.write(f"Priority: {cat_info['priority']}")
        st.write(f"Status: {cat_info['status']}")
        st.write(f"Assigned Agent: {agent}")

    # -------------------------------
    # Customer Satisfaction Input
    # -------------------------------
    if "latest_ticket" in st.session_state:
        st.subheader("📝 Rate your satisfaction")
        if "rating" not in st.session_state:
            st.session_state.rating = 5

        st.session_state.rating = st.slider(
            "Please rate your satisfaction (1 = lowest, 5 = highest)",
            min_value=1, max_value=5,
            value=st.session_state.rating
        )

        if st.button("✅ Submit Rating & Close Ticket"):
            ticket = st.session_state.latest_ticket
            ticket["ticket_status"] = "Closed"
            ticket["customer_satisfaction_rating"] = st.session_state.rating
            ticket["time_to_resolution"] = str(
                int((datetime.datetime.now() - datetime.datetime.strptime(
                    ticket["first_response_time"], "%Y-%m-%d %H:%M:%S")).total_seconds())
            ) + "s"

            save_ticket_to_sheets(ticket)
            st.session_state.latest_ticket = ticket
            st.success(f"🎉 Ticket closed and rated {st.session_state.rating}/5! Thank you for your feedback.")

# ===============================
# Dashboard Page
# ===============================
elif menu == "Dashboard":
    st.subheader("📊 Ticket Overview & Agent Performance")

    # Fetch tickets
    data = sheet.get_all_records()
    if not data:
        st.warning("No tickets found in Google Sheets.")
        st.stop()
    df = pd.DataFrame(data)

    # -------------------------------
    # Ticket Overview
    # -------------------------------
    st.markdown("### 🗂 Ticket Overview")
    st.write(f"Total Tickets: {len(df)}")

    # Tickets by Status (Closed vs Open)
    df['ticket_status'] = df['ticket_status'].replace({'In Progress': 'Open'})  # merge In Progress as Open
    status_counts = df['ticket_status'].value_counts().reindex(['Open', 'Closed'], fill_value=0).reset_index()
    status_counts.columns = ['ticket_status', 'count']
    status_fig = px.pie(status_counts, names='ticket_status', values='count', title='Tickets by Status')
    st.plotly_chart(status_fig, use_container_width=True)

    # Tickets by Priority (Low, Medium, High, Critical)
    priority_order = ['Low', 'Medium', 'High', 'Critical']
    df['ticket_priority'] = pd.Categorical(df['ticket_priority'], categories=priority_order, ordered=True)
    priority_counts = df['ticket_priority'].value_counts().reindex(priority_order, fill_value=0).reset_index()
    priority_counts.columns = ['ticket_priority', 'count']
    priority_fig = px.bar(priority_counts, x='ticket_priority', y='count', text='count', title='Tickets by Priority')
    st.plotly_chart(priority_fig, use_container_width=True)

    # Tickets by Channel
    channel_counts = df['ticket_channel'].value_counts().reset_index()
    channel_counts.columns = ['ticket_channel', 'count']
    channel_fig = px.pie(channel_counts, names='ticket_channel', values='count', title='Tickets by Channel')
    st.plotly_chart(channel_fig, use_container_width=True)

    # -------------------------------
    # Agent Performance (Selected Roles)
    # -------------------------------
    st.markdown("### 👩‍💼 Agent Performance")
    df['assigned_agent'] = df['assigned_agent'].fillna('General Support')
    valid_agents = ['Sales', 'Marketing', 'Engineering', 'General Support']
    df_agents = df[df['assigned_agent'].isin(valid_agents)]

    agent_counts = df_agents['assigned_agent'].value_counts().reindex(valid_agents, fill_value=0).reset_index()
    agent_counts.columns = ['assigned_agent', 'count']
    tickets_agent_fig = px.bar(agent_counts, x='assigned_agent', y='count', text='count', title='Tickets Assigned per Agent')
    st.plotly_chart(tickets_agent_fig, use_container_width=True)
