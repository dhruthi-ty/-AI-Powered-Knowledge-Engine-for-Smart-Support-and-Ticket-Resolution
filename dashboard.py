# dashboard.py
import pandas as pd
import matplotlib.pyplot as plt
from rag import sheet  # import your Google Sheet object from rag.py

# ================================
# Fetch Tickets
# ================================
def fetch_all_tickets():
    """Fetch all tickets from Google Sheets as a DataFrame"""
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# ================================
# Ticket Overview Metrics
# ================================
def ticket_overview_metrics(df):
    """Compute overview metrics for tickets"""
    return {
        "total_tickets": len(df),
        "tickets_by_status": df['ticket_status'].value_counts().to_dict(),
        "tickets_by_priority": df['ticket_priority'].value_counts().to_dict(),
        "tickets_by_channel": df['ticket_channel'].value_counts().to_dict()
    }

# ================================
# Agent Performance Metrics
# ================================
def agent_performance_metrics(df):
    """Compute metrics for each agent"""
    # Convert numeric fields
    df['time_to_resolution'] = pd.to_numeric(df['time_to_resolution'], errors='coerce')
    df['customer_satisfaction_rating'] = pd.to_numeric(df['customer_satisfaction_rating'], errors='coerce')
    
    tickets_per_agent = df['assigned_agent'].value_counts().to_dict()
    avg_resolution = df.groupby('assigned_agent')['time_to_resolution'].mean().to_dict()
    avg_csat = df.groupby('assigned_agent')['customer_satisfaction_rating'].mean().to_dict()
    resolved_pending = df.groupby(['assigned_agent', 'ticket_status']).size().unstack(fill_value=0).to_dict('index')
    
    return {
        "tickets_per_agent": tickets_per_agent,
        "avg_resolution_time": avg_resolution,
        "avg_csat": avg_csat,
        "resolved_pending": resolved_pending
    }

# ================================
# Plot Functions
# ================================
def plot_ticket_overview(overview):
    """Plot ticket overview charts"""
    plt.figure(figsize=(6,6))
    plt.pie(overview['tickets_by_status'].values(), labels=overview['tickets_by_status'].keys(), autopct='%1.1f%%')
    plt.title("Tickets by Status")
    plt.show()
    
    plt.figure(figsize=(6,4))
    plt.bar(overview['tickets_by_priority'].keys(), overview['tickets_by_priority'].values(), color='orange')
    plt.title("Tickets by Priority")
    plt.ylabel("Number of Tickets")
    plt.show()
    
    plt.figure(figsize=(6,6))
    plt.pie(overview['tickets_by_channel'].values(), labels=overview['tickets_by_channel'].keys(), autopct='%1.1f%%')
    plt.title("Tickets by Channel")
    plt.show()

def plot_agent_performance(metrics):
    """Plot agent performance charts"""
    plt.figure(figsize=(6,4))
    plt.bar(metrics['tickets_per_agent'].keys(), metrics['tickets_per_agent'].values(), color='green')
    plt.title("Tickets Assigned per Agent")
    plt.ylabel("Number of Tickets")
    plt.show()
    
    plt.figure(figsize=(6,4))
    plt.bar(metrics['avg_resolution_time'].keys(), metrics['avg_resolution_time'].values(), color='red')
    plt.title("Average Resolution Time per Agent")
    plt.ylabel("Time to Resolution (hrs)")
    plt.show()
    
    plt.figure(figsize=(6,4))
    plt.bar(metrics['avg_csat'].keys(), metrics['avg_csat'].values(), color='blue')
    plt.title("Average Customer Satisfaction per Agent")
    plt.ylabel("CSAT Rating")
    plt.show()
    
    # Stacked bar for resolved vs pending
    df_resolved = pd.DataFrame(metrics['resolved_pending']).T.fillna(0)
    df_resolved.plot(kind='bar', stacked=True, figsize=(8,4))
    plt.title("Tickets Resolved vs Pending per Agent")
    plt.ylabel("Number of Tickets")
    plt.show()

# ================================
# Main Execution
# ================================
if __name__ == "__main__":
    df = fetch_all_tickets()
    
    # Ticket Overview
    overview = ticket_overview_metrics(df)
    print(f"Total Tickets: {overview['total_tickets']}")
    plot_ticket_overview(overview)
    
    # Agent Performance
    metrics = agent_performance_metrics(df)
    plot_agent_performance(metrics)
