import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Ticket Hub - Support System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (Purple Theme matching your design guidelines)
st.markdown(
    """
    <style>
    .main {
        background-color: #F8F6FF;
    }
    .stButton>button {
        background-color: #7C3AED;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #6D28D9;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1px solid #E5E7EB;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State for Tickets so data persists during interaction
if "tickets" not in st.session_state:
    st.session_state.tickets = pd.DataFrame(
        [
            {
                "ID": "TKT-1001",
                "Subject": "Unable to login to user account",
                "Category": "Account",
                "Assignee": "John Doe",
                "Priority": "Critical",
                "Status": "New",
            },
            {
                "ID": "TKT-1002",
                "Subject": "Billing discrepancy on invoice #402",
                "Category": "Billing",
                "Assignee": "Jane Smith",
                "Priority": "High",
                "Status": "In Progress",
            },
            {
                "ID": "TKT-1003",
                "Subject": "API webhook returning 500 error",
                "Category": "Technical",
                "Assignee": "Alex Johnson",
                "Priority": "Medium",
                "Status": "Resolved",
            },
            {
                "ID": "TKT-1004",
                "Subject": "Request for password policy documentation",
                "Category": "General",
                "Assignee": "John Doe",
                "Priority": "Low",
                "Status": "Closed",
            },
        ]
    )

# Sidebar Navigation
st.sidebar.title("🎫 Ticket Hub")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Ticket List",
        "Create Ticket",
        "Knowledge Base",
        "Agents",
        "Reports",
    ],
)

df = st.session_state.tickets

# 1. DASHBOARD
if menu == "Dashboard":
    st.title("📊 Dashboard Overview")
    st.markdown("Welcome back, **Admin User** 👋")
    st.markdown("")

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", len(df))
    with col2:
        critical_count = len(df[df["Priority"] == "Critical"])
        st.metric("Critical Tickets", critical_count)
    with col3:
        progress_count = len(df[df["Status"] == "In Progress"])
        st.metric("In Progress", progress_count)
    with col4:
        resolved_count = len(
            df[df["Status"].isin(["Resolved", "Closed"])]
        )
        st.metric("Resolved / Closed", resolved_count)

    st.markdown("### 🕒 Recent Tickets")
    st.dataframe(df.head(5), use_container_width=True)

# 2. TICKET LIST & MANAGEMENT
elif menu == "Ticket List":
    st.title("📋 Support Ticket List")

    # Search & Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input(
            "Search by Subject or ID", placeholder="Type keyword..."
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            [
                "All",
                "New",
                "In Progress",
                "On Hold",
                "Resolved",
                "Closed",
            ],
        )
    with col3:
        priority_filter = st.selectbox(
            "Filter by Priority", ["All", "Critical", "High", "Medium", "Low"]
        )

    # Apply filters
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Subject"]
            .str.contains(search_query, case=False, na=False)
            | filtered_df["ID"].str.contains(
                search_query, case=False, na=False
            )
        ]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df["Priority"] == priority_filter]

    st.dataframe(filtered_df, use_container_width=True)

    # Delete Ticket Section
    st.markdown("### Manage Ticket")
    ticket_to_delete = st.selectbox(
        "Select Ticket ID to Delete", ["Select..."] + list(df["ID"])
    )
    if ticket_to_delete != "Select...":
        if st.button("Delete Selected Ticket"):
            st.session_state.tickets = df[df["ID"] != ticket_to_delete]
            st.success(f"Ticket {ticket_to_delete} deleted successfully!")
            st.rerun()

# 3. CREATE TICKET
elif menu == "Create Ticket":
    st.title("➕ Create New Support Ticket")

    with st.form("create_ticket_form"):
        subject = st.text_input(
            "Subject", placeholder="Brief description of the issue"
        )
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Category",
                ["Technical", "Billing", "Account", "General"],
            )
        with col2:
            priority = st.selectbox(
                "Priority", ["Low", "Medium", "High", "Critical"]
            )

        assignee = st.selectbox(
            "Assign Agent", ["John Doe", "Jane Smith", "Alex Johnson"]
        )
        description = st.text_area(
            "Description",
            placeholder="Provide detailed information about your issue...",
        )

        submitted = st.form_submit_button("Submit Ticket")
        if submitted:
            if subject.strip() == "" or description.strip() == "":
                st.error("Please fill in both Subject and Description.")
            else:
                new_id = f"TKT-100{len(df) + 1}"
                new_row = pd.DataFrame(
                    [
                        {
                            "ID": new_id,
                            "Subject": subject,
                            "Category": category,
                            "Assignee": assignee,
                            "Priority": priority,
                            "Status": "New",
                        }
                    ]
                )
                st.session_state.tickets = pd.concat(
                    [new_row, st.session_state.tickets], ignore_index=True
                )
                st.success(f"Ticket {new_id} created successfully!")

# 4. KNOWLEDGE BASE
elif menu == "Knowledge Base":
    st.title("📖 Knowledge Base & FAQs")

    st.markdown("### How to reset your password?")
    st.info(
        'Navigate to the login page, click "Forgot Password", and follow the instructions sent to your email address.'
    )

    st.markdown("### Updating billing information")
    st.info(
        "Go to Account Settings > Billing Profile to add or update your credit card information securely."
    )

    st.markdown("### Understanding ticket priorities")
    st.info(
        "Critical issues block core business operations, while low-priority requests relate to minor cosmetic changes."
    )

# 5. AGENTS
elif menu == "Agents":
    st.title("👥 Support Agents & Workload")

    agents_data = pd.DataFrame(
        [
            {
                "Agent Name": "John Doe",
                "Role": "Technical Specialist",
                "Active Tickets": 4,
                "Status": "Available",
            },
            {
                "Agent Name": "Jane Smith",
                "Role": "Billing Expert",
                "Active Tickets": 2,
                "Status": "Busy",
            },
            {
                "Agent Name": "Alex Johnson",
                "Role": "General Support",
                "Active Tickets": 1,
                "Status": "Available",
            },
        ]
    )
    st.dataframe(agents_data, use_container_width=True)

# 6. REPORTS
elif menu == "Reports":
    st.title("📈 Ticket Resolution Reports")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Resolution Time", "4.2 Hours")
    with col2:
        st.metric("Customer Satisfaction (CSAT)", "94.8%")
    with col3:
        st.metric("SLA Compliance Rate", "98.1%")