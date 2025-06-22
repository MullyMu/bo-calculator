#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from dataclasses import dataclass
from typing import List

# --- Data Model ---
@dataclass
class Shareholder:
    shares: float
    is_joint: bool = False
    joint_parties: int = 1
    name: str = ""

    def calculate_individual_share(self, total_shares: float) -> float:
        if self.is_joint:
            return (self.shares / total_shares * 100) / self.joint_parties
        return (self.shares / total_shares * 100)

    def get_display_names(self) -> List[str]:
        base_name = self.name if self.name else "Unnamed"
        if self.is_joint:
            return [f"{base_name} (Joint Party {i+1})" for i in range(self.joint_parties)]
        return [base_name]

# --- Setup ---
THRESHOLDS = {
    "Australia (AU)": 25.0,
    "United Kingdom (UK)": 25.0,
    "United States (US)": 25.0
}

st.set_page_config(page_title="Beneficial Ownership Calculator", layout="centered")
st.markdown("## 🧮 Beneficial Ownership Calculator")
st.markdown("Use this tool to determine which shareholders meet the legal definition of a Beneficial Owner based on jurisdiction thresholds.")

st.divider()

# --- Input: Jurisdiction & Shares ---
col1, col2 = st.columns(2)
with col1:
    jurisdiction_label = st.selectbox("🌍 Select Jurisdiction", list(THRESHOLDS.keys()))
with col2:
    total_shares = st.number_input("📦 Total Issued Shares/Units", min_value=1.0, step=1.0)

threshold = THRESHOLDS[jurisdiction_label]
min_required = (threshold / 100.0) * total_shares

if total_shares:
    st.info(f"To qualify as a Beneficial Owner in **{jurisdiction_label}**, a shareholder needs at least **{threshold}%** of total shares, which is **{min_required:.2f} shares**.")

st.divider()

# --- Input: Shareholders ---
st.markdown("### 👥 Shareholder Details")
num_holders = st.number_input("🔢 Number of Shareholders", min_value=1, step=1)

shareholders = []
for i in range(num_holders):
    with st.expander(f"Shareholder {i+1}"):
        col1, col2 = st.columns([2, 1])
        name = col1.text_input("Name", key=f"name_{i}", placeholder="e.g. Jane Doe")
        shares = col2.number_input("Shares", min_value=0.0, step=1.0, key=f"shares_{i}")
        is_joint = st.checkbox("Is this a joint holding?", key=f"joint_{i}")
        joint_parties = 1
        if is_joint:
            joint_parties = st.number_input("Number of joint parties", min_value=2, step=1, key=f"jp_{i}")
        shareholders.append(Shareholder(shares, is_joint, joint_parties, name))

st.divider()

# --- Output Button ---
if st.button("📊 Calculate Beneficial Owners"):
    st.markdown("### ✅ Beneficial Ownership Results")
    results = []

    for idx, holder in enumerate(shareholders):
        share_percent = holder.calculate_individual_share(total_shares)
        qualifies = share_percent >= threshold
        for display_name in holder.get_display_names():
            rationale = "🟢 Qualifies as BO" if qualifies else "🔴 Does not qualify"
            results.append({
                "Name": display_name,
                "Ownership %": round(share_percent, 2),
                "Status": rationale
            })

    if results:
        st.dataframe(results, use_container_width=True)

    else:
        st.warning("No shareholders entered yet.")


# In[ ]:




