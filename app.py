import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

st.title("💰 AI Expense Tracker (Rs Based)")

# Load data
try:
    df = pd.read_csv("data/expenses.csv")
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])

# Input
entry = st.text_input("Enter your expense (e.g., 'Bought groceries Rs500')")

def parse_entry(text):
    amount_match = re.search(r"rs\s*(\d+)", text, re.IGNORECASE)
    if amount_match:
        amount = int(amount_match.group(1))
    else:
        st.warning("⚠️ No amount found! Please use 'Rs' followed by the number.")
        return None, None
    words = text.lower().split()
    category = " ".join([word for word in words if word.isalpha()])
    return category, amount

if st.button("Add Expense"):
    if entry:
        category, amount = parse_entry(entry)
        if category and amount:
            new_row = pd.DataFrame([[datetime.now().date(), category, amount]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("data/expenses.csv", index=False)
            st.success(f"✅ Added Rs{amount} to '{category}'")

# Show Data
if not df.empty:
    st.subheader("📊 All Expenses")
    st.dataframe(df)

    st.subheader("📈 Expense Summary")
    summary = df.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    summary.plot(kind="bar", ax=ax)
    st.pyplot(fig)
else:
    st.info("ℹ️ No expenses yet! Add some above ☝️ using 'Rs'")
