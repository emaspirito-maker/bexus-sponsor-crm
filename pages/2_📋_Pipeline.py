import pandas as pd
import streamlit as st

from auth import require_login
from db import STATI, add_company, get_client, list_companies, update_company


def _is_same_value(edited_value, original_value):
    """Compare values, treating NaN and None as equal (Streamlit round-trip artifact)."""
    if pd.isna(edited_value) and original_value is None:
        return True
    return edited_value == original_value


st.set_page_config(page_title="Pipeline", page_icon="📋")
require_login()

try:
    client = get_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"Impossibile caricare i dati: {e}")
    st.stop()

st.title("Pipeline sponsor")

stato_filter = st.selectbox("Filtra per stato", ["Tutti"] + STATI)
settore_filter = st.text_input("Filtra per settore (testo libero)")

try:
    companies = list_companies(client, stato_filter=None if stato_filter == "Tutti" else stato_filter)
except Exception as e:
    st.error(f"Impossibile caricare i dati: {e}")
    st.stop()

df = pd.DataFrame(companies)
if settore_filter:
    df = df[df["settore"].str.contains(settore_filter, case=False, na=False)]

if df.empty:
    st.info("Nessuna azienda trovata per questo filtro.")
else:
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
        try:
            for _, edited_row in edited_df.iterrows():
                original = original_by_id.get(edited_row["id"], {})
                changed = {
                    k: (None if pd.isna(edited_row[k]) else edited_row[k])
                    for k in edited_row.index
                    if k not in ("id", "created_at", "updated_at")
                    and not _is_same_value(edited_row[k], original.get(k))
                }
                if changed:
                    update_company(client, int(edited_row["id"]), **changed)
            st.success("Modifiche salvate.")
            st.rerun()
        except Exception as e:
            st.error(f"Errore nel salvataggio: {e}")

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
