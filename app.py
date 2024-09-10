import streamlit as st

role = st.selectbox("Select Role:", ["Candidate", "Admin"])

if role == "Candidate":
    st.title("Candidate Portal")



elif role == "Admin":
    st.title("Admin Portal")
