# BEXUS Sponsor CRM

CRM personale per la pipeline sponsor/partner del progetto BEXUS 2027.
Streamlit + Supabase, deploy su Streamlit Community Cloud.

## Setup — Supabase

1. Crea un progetto gratuito su https://supabase.com
2. Vai su "SQL Editor", incolla il contenuto di `schema.sql` ed eseguilo
3. Vai su "Project Settings" → "API": copia "Project URL" e la chiave
   "anon public" (o "service_role" se vuoi bypassare le row-level-security
   policy — per un progetto a singolo utente va bene)

## Setup — password dell'app

Genera l'hash della password che userai per entrare nell'app:

```bash
python3 -c "import hashlib; print(hashlib.sha256(b'la-tua-password').hexdigest())"
```

## Sviluppo locale

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# poi modifica .streamlit/secrets.toml con i tuoi valori reali
streamlit run app.py
```

## Test

```bash
pytest
```

## Migrazione dati iniziale

Serve un file `.env` (mai committato) nella root con:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-key
```

Poi:

```bash
python3 migrate_csv_to_supabase.py /percorso/a/companies.csv
```

## Deploy

1. Pusha questo repo su GitHub
2. Su https://share.streamlit.io, "New app", collega il repo, file di
   ingresso `app.py`
3. In "Advanced settings" → "Secrets", incolla il contenuto del tuo
   `.streamlit/secrets.toml` locale (con i valori reali)
4. Deploy
