"""One-off script: import a companies.csv (schema matching sponsor_pipeline/companies.csv
in the technical repo) into the Supabase `companies` table.

Requires a local .env (gitignored) with SUPABASE_URL and SUPABASE_KEY.

Usage: python3 migrate_csv_to_supabase.py path/to/companies.csv
"""
import csv
import os
import sys

from db import add_company, get_client


def migrate(csv_path: str, client) -> int:
    imported = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_company(
                client,
                row["nome_azienda"],
                settore=row.get("settore") or None,
                contatto_nome=row.get("contatto_nome") or None,
                contatto_ruolo=row.get("contatto_ruolo") or None,
                contatto_email_linkedin=row.get("contatto_email_linkedin") or None,
                canale_primo_contatto=row.get("canale_primo_contatto") or None,
                stato=row.get("stato") or "da_verificare",
                pacchetto_tier=row.get("pacchetto_tier") or None,
                valore=row.get("valore") or None,
                data_ultimo_contatto=row.get("data_ultimo_contatto") or None,
                prossimo_step=row.get("prossimo_step") or None,
                note=row.get("note") or None,
            )
            imported += 1
    return imported


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "companies.csv"
    client = get_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    count = migrate(csv_path, client)
    print(f"Importate {count} aziende da {csv_path}.")
