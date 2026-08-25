create table companies (
    id bigint generated always as identity primary key,
    nome_azienda text not null,
    settore text,
    contatto_nome text,
    contatto_ruolo text,
    contatto_email_linkedin text,
    canale_primo_contatto text,
    stato text not null default 'da_verificare'
        check (stato in ('da_verificare', 'da_contattare', 'contattata', 'in_negoziazione', 'sponsor_confermato', 'persa')),
    pacchetto_tier text,
    valore numeric,
    data_ultimo_contatto date,
    prossimo_step text,
    note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger companies_set_updated_at
before update on companies
for each row
execute function set_updated_at();
