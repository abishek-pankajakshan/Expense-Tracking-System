import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_url = "http://localhost:8000"

def analytics_months_tab():
    try:
        response = requests.get(f"{API_url}/analytics_by_month")
        if response.status_code == 200:
            data = response.json()
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return

        # Convert data to DataFrame
    if not data:
        st.warning("No data available for visualization.")
        return

    df = pd.DataFrame(data)
    df["month_index"] = df["month_index"].astype(int)  # Ensure correct sorting
    df = df.sort_values(by="month_index")  # Sort by month index

    # Display Data Table
    st.subheader("Expense Summary Table")
    st.dataframe(df)

    # Plot Bar Chart
    st.subheader("Monthly Expense Trend")
    fig, ax = plt.subplots()
    ax.bar(df["month"], df["total_amount"], color="skyblue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount")
    ax.set_title("Total Amount by Month")
    plt.xticks(rotation=45)

    st.pyplot(fig)
