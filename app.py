import streamlit as st

from auth import require_login

st.set_page_config(page_title="BEXUS Sponsor CRM", page_icon="🛰️")
require_login()

st.title("BEXUS Sponsor CRM")
st.write("Usa il menu a sinistra per Dashboard e Pipeline.")
