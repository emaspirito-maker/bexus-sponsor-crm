"""Password gate for the sponsor CRM. A single shared password protects the app."""
import hashlib

import streamlit as st


def verify_password(input_password: str, stored_hash: str) -> bool:
    return hashlib.sha256(input_password.encode("utf-8")).hexdigest() == stored_hash


def require_login() -> None:
    if st.session_state.get("authenticated"):
        return
    st.title("BEXUS Sponsor CRM")
    password = st.text_input("Password", type="password")
    if st.button("Entra"):
        if verify_password(password, st.secrets["APP_PASSWORD_HASH"]):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Password errata.")
    st.stop()
