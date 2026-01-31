import streamlit as st
from datetime import date
from utils import initialize_data, load_data, add_expense, delete_expense

st.title("Personal Financial Expense Tracker")

# Initialize & load data
initialize_data()
df = load_data()

# Create Month column for analysis (YYYY-MM)
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Add Expense Section

st.subheader("Add a New Expense")

expense_date = st.date_input("Date", date.today())
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.selectbox(
    "Category",
    ["Food", "Transport", "Rent", "Shopping", "Entertainment", "Other"]
)
description = st.text_input("Description (optional)")

if st.button("Add Expense"):
    new_expense = {
        "Date": expense_date,
        "Amount": amount,
        "Category": category,
        "Description": description
    }

    df = add_expense(df, new_expense)
    st.success("Expense added successfully")
    st.rerun()

# Expense History

st.subheader("Expense History")

st.dataframe(
    df[["Date_display", "Amount", "Category", "Description"]]
    .rename(columns={"Date_display": "Date"}),
    hide_index=True
)

# Delete Expense

st.subheader("Delete an Expense")

if not df.empty:
    delete_index = st.selectbox("Select expense index to delete", df.index)

    if st.button("Delete Selected Expense"):
        df = delete_expense(df, delete_index)
        st.success("Expense deleted successfully")
        st.rerun()

st.subheader("Expense Analysis")

chart_type = st.radio(
    "Select analysis type",
    ["Monthly Overview", "Category-wise Analysis"]
)

# STEP 3: Monthly Overview Chart
if chart_type == "Monthly Overview":
    monthly_summary = (
        df.groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    st.subheader("Monthly Spending Overview")
    st.bar_chart(
        monthly_summary.set_index("Month")
    )

# STEP 4: Category-wise Chart

if chart_type == "Category-wise Analysis":
    selected_category = st.selectbox(
        "Select Category",
        ["All"] + sorted(df["Category"].unique().tolist())
    )

    if selected_category == "All":
        category_summary = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        st.subheader("Category-wise Spending (All Categories)")
        st.bar_chart(
            category_summary.set_index("Category")
        )

    else:
        category_monthly = (
            df[df["Category"] == selected_category]
            .groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        st.subheader(f"{selected_category} Spending Over Time")
        st.line_chart(
            category_monthly.set_index("Month")
        )

