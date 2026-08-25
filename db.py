"""Data access layer for the BEXUS sponsor pipeline, backed by a Supabase Postgres table."""
from __future__ import annotations

STATI = ["da_verificare", "da_contattare", "contattata", "in_negoziazione", "sponsor_confermato", "persa"]


def get_client(url: str, key: str):
    from supabase import create_client
    return create_client(url, key)


def list_companies(client, stato_filter: str | None = None) -> list[dict]:
    query = client.table("companies").select("*").order("nome_azienda")
    if stato_filter:
        query = query.eq("stato", stato_filter)
    return query.execute().data


def add_company(client, nome_azienda: str, **fields) -> dict:
    stato = fields.get("stato", "da_verificare")
    if stato not in STATI:
        raise ValueError(f"stato non valido: {stato}")
    existing = (
        client.table("companies")
        .select("id")
        .ilike("nome_azienda", nome_azienda)
        .execute()
        .data
    )
    if existing:
        raise ValueError(f"'{nome_azienda}' e' gia' in pipeline")
    row = {"nome_azienda": nome_azienda, "stato": stato}
    row.update({k: v for k, v in fields.items() if k != "stato" and v is not None})
    return client.table("companies").insert(row).execute().data[0]


def update_company(client, company_id: int, **fields) -> dict:
    if "stato" in fields and fields["stato"] not in STATI:
        raise ValueError(f"stato non valido: {fields['stato']}")
    return client.table("companies").update(fields).eq("id", company_id).execute().data[0]


def get_stats(client) -> dict:
    rows = client.table("companies").select("stato, valore").execute().data
    per_stato = {s: 0 for s in STATI}
    valore_totale = 0.0
    for row in rows:
        per_stato[row["stato"]] = per_stato.get(row["stato"], 0) + 1
        if row["stato"] == "sponsor_confermato" and row.get("valore"):
            valore_totale += float(row["valore"])
    return {"totale": len(rows), "per_stato": per_stato, "valore_totale": valore_totale}
