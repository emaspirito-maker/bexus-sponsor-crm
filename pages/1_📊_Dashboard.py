import streamlit as st

from auth import require_login
from db import get_client, get_stats

st.set_page_config(page_title="Dashboard", page_icon="📊")
require_login()

client = get_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
stats = get_stats(client)

st.title("Dashboard")
st.metric("Totale aziende", stats["totale"])

cols = st.columns(len(stats["per_stato"]))
for col, (stato, count) in zip(cols, stats["per_stato"].items()):
    col.metric(stato, count)

st.metric("Valore raccolto (sponsor confermati)", f"€ {stats['valore_totale']:.2f}")
