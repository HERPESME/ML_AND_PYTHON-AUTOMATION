# src/human_interface/web_interface.py

import streamlit as st


def alert_approval_ui(anomaly_record):
    st.title("Anomaly Alert Review")
    st.write("⚠️ Anomaly Detected:")
    st.json(anomaly_record)

    approve = st.button("Approve as Threat")
    dismiss = st.button("Dismiss as False Alarm")

    if approve:
        return "approved"
    elif dismiss:
        return "dismissed"
    return None
