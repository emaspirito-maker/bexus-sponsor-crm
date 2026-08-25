from unittest.mock import MagicMock, patch

import migrate_csv_to_supabase as migrate_mod


def test_migrate_imports_each_csv_row(tmp_path):
    csv_content = (
        "nome_azienda,settore,contatto_nome,contatto_ruolo,contatto_email_linkedin,"
        "canale_primo_contatto,stato,pacchetto_tier,valore,data_ultimo_contatto,prossimo_step,note\n"
        "Aviointeriors S.p.A.,Aerospace diretto,,,,,da_contattare,,,,Prossimo step,Nota di test\n"
        "Mogno Srl,Subfornitura aerospace,,,,,da_contattare,,,,Prossimo step,Nota di test\n"
    )
    csv_path = tmp_path / "companies.csv"
    csv_path.write_text(csv_content, encoding="utf-8")

    client = MagicMock()
    with patch.object(migrate_mod, "add_company") as mock_add:
        imported = migrate_mod.migrate(str(csv_path), client)

    assert imported == 2
    assert mock_add.call_count == 2
    first_call_kwargs = mock_add.call_args_list[0].kwargs
    assert first_call_kwargs["stato"] == "da_contattare"
    assert first_call_kwargs["note"] == "Nota di test"
