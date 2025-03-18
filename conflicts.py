# -*- coding: utf-8 -*-
"""Conflicts.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VLxBjB_feXKf5Et1mHf7lC8VLav7KS-L
"""

!pip install streamlit

!streamlit run your_script.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load billing data
billing_url = "https://docs.google.com/spreadsheets/d/192nbhNcK3m6OrtwkXvB_CTKCZcx_If3fxKvKJwbFHhA/export?format=csv"
billing_data = pd.read_csv(billing_url)

# Load conflicts data
conflicts_url = "https://docs.google.com/spreadsheets/d/1-PEdSnct_lj4SvtOfGYlAdXa8vLQGvBMX-I5vi-1Y9k/export?format=csv"
conflicts_data = pd.read_csv(conflicts_url)

# Streamlit UI
st.set_page_config(page_title="Competitive Conflict Checker", page_icon="🔍", layout="centered")
st.title("🔍 Competitive Conflict Checker")

# User inputs
person_name = st.text_input("Enter the employee's name:")
client_to_check = st.text_input("Enter the client/brand to check:")

if person_name and client_to_check:
    # Convert "EnteredOn" to datetime
    billing_data["EnteredOn"] = pd.to_datetime(billing_data["EnteredOn"])

    # Get last 6 months of data
    end_date = billing_data["EnteredOn"].max()
    start_date = end_date - timedelta(days=180)

    # Filter for the given employee within the last 6 months
    filtered_data = billing_data[
        (billing_data["Employee Name"] == person_name) &
        (billing_data["EnteredOn"] >= start_date) &
        (billing_data["EnteredOn"] <= end_date)
    ]

if person_name and client_to_check:
    # Convert "EnteredOn" to datetime
    billing_data["EnteredOn"] = pd.to_datetime(billing_data["EnteredOn"])

    # Get last 6 months of data
    end_date = billing_data["EnteredOn"].max()
    start_date = end_date - timedelta(days=180)

    # Filter for the given employee within the last 6 months
    filtered_data = billing_data[
        (billing_data["Employee Name"] == person_name) &
        (billing_data["EnteredOn"] >= start_date) &
        (billing_data["EnteredOn"] <= end_date)
    ]

    # Find conflicts
    conflicting_brands = set()
    for _, row in conflicts_data.iterrows():
        if row["Company A"] == client_to_check or row["Company B"] == client_to_check:
            conflicting_brands.update([row["Competitive Companies"], row["Brands"]])

    conflicts = filtered_data[filtered_data["Company Name"].isin(conflicting_brands)]

    # Display results
    st.subheader("Billing Records (Last 6 Months)")
    if not filtered_data.empty:
        st.dataframe(filtered_data.style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#f4f4f4')]}]))
    else:
        st.write("No billing records found for this employee.")

    st.subheader("Conflict Check Results")
    if not conflicts.empty:
        st.error("🚨 Conflict detected! The employee has worked on a competing brand.")
        st.dataframe(conflicts.style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#f4f4f4')]}]))

        # Calculate waiting period (180 days from the last billing date)
        last_billing_date = conflicts["EnteredOn"].max()
        waiting_period = last_billing_date + timedelta(days=180)
        st.warning(f"⚠️ They need to wait until **{waiting_period.strftime('%B %d, %Y')}** before working on {client_to_check}.")
    else:
        st.success("✅ No conflicts found. The employee is clear to work on this client.")