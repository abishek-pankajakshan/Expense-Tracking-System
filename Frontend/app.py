import streamlit as st
from add_update_UI import add_update_tab
from analytics_category_UI import analytics_category_tab
from analytics_months_UI import  analytics_months_tab

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by Categotry", "Analytics by Month"])

with tab1:
    add_update_tab()
with tab2:
    analytics_category_tab()
with tab3:
    analytics_months_tab()