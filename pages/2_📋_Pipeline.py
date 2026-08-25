import pandas as pd
import streamlit as st

from auth import require_login
from db import STATI, add_company, get_client, list_companies, update_company

st.set_page_config(page_title="Pipeline", page_icon="📋")
require_login()

client = get_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("Pipeline sponsor")

stato_filter = st.selectbox("Filtra per stato", ["Tutti"] + STATI)
companies = list_companies(client, stato_filter=None if stato_filter == "Tutti" else stato_filter)

df = pd.DataFrame(companies)
edited_df = st.data_editor(
    df,
    column_config={"stato": st.column_config.SelectboxColumn("stato", options=STATI)},
    disabled=["id", "created_at", "updated_at"],
    num_rows="fixed",
    use_container_width=True,
    key="pipeline_editor",
)

if st.button("Salva modifiche"):
    original_by_id = {row["id"]: row for row in companies}
    for _, edited_row in edited_df.iterrows():
        original = original_by_id.get(edited_row["id"], {})
        changed = {
            k: edited_row[k]
            for k in edited_row.index
            if k not in ("id", "created_at", "updated_at") and edited_row[k] != original.get(k)
        }
        if changed:
            update_company(client, int(edited_row["id"]), **changed)
    st.success("Modifiche salvate.")
    st.rerun()

st.download_button(
    "Esporta CSV",
    df.to_csv(index=False).encode("utf-8"),
    file_name="companies_export.csv",
    mime="text/csv",
)

st.divider()
st.subheader("Aggiungi azienda")
with st.form("add_company_form", clear_on_submit=True):
    nome = st.text_input("Nome azienda *")
    settore = st.text_input("Settore")
    stato_iniziale = st.selectbox("Stato iniziale", STATI, index=STATI.index("da_verificare"))
    prossimo_step = st.text_input("Prossimo step")
    note = st.text_area("Note")
    submitted = st.form_submit_button("Aggiungi")
    if submitted:
        if not nome.strip():
            st.error("Il nome azienda e' obbligatorio.")
        else:
            try:
                add_company(
                    client,
                    nome.strip(),
                    settore=settore or None,
                    stato=stato_iniziale,
                    prossimo_step=prossimo_step or None,
                    note=note or None,
                )
                st.success(f"'{nome}' aggiunta.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
