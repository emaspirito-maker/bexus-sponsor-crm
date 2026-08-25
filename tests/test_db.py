# tests/test_db.py
from unittest.mock import MagicMock

import pytest

import db


def test_list_companies_returns_all_when_no_filter():
    client = MagicMock()
    client.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "nome_azienda": "Aviointeriors"}
    ]
    result = db.list_companies(client)
    assert result == [{"id": 1, "nome_azienda": "Aviointeriors"}]
    client.table.assert_called_once_with("companies")


def test_list_companies_filters_by_stato():
    client = MagicMock()
    chain = client.table.return_value.select.return_value.order.return_value
    chain.eq.return_value.execute.return_value.data = [
        {"id": 2, "nome_azienda": "Mogno Srl", "stato": "da_contattare"}
    ]
    result = db.list_companies(client, stato_filter="da_contattare")
    assert result == [{"id": 2, "nome_azienda": "Mogno Srl", "stato": "da_contattare"}]
    chain.eq.assert_called_once_with("stato", "da_contattare")


def test_add_company_inserts_new_row():
    client = MagicMock()
    client.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = []
    client.table.return_value.insert.return_value.execute.return_value.data = [
        {"id": 3, "nome_azienda": "Celab Srl", "stato": "da_verificare"}
    ]
    result = db.add_company(client, "Celab Srl")
    assert result["nome_azienda"] == "Celab Srl"
    client.table.return_value.insert.assert_called_once()


def test_add_company_rejects_duplicate_name():
    client = MagicMock()
    client.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = [
        {"id": 1, "nome_azienda": "Celab Srl"}
    ]
    with pytest.raises(ValueError, match="gia'"):
        db.add_company(client, "Celab Srl")


def test_add_company_rejects_invalid_stato():
    client = MagicMock()
    with pytest.raises(ValueError, match="stato non valido"):
        db.add_company(client, "Test Srl", stato="stato_inventato")


def test_add_company_passes_through_optional_fields():
    client = MagicMock()
    client.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = []
    client.table.return_value.insert.return_value.execute.return_value.data = [{"id": 4}]
    db.add_company(client, "Unitec Srl", settore="Meccanica", note="test")
    inserted_row = client.table.return_value.insert.call_args.args[0]
    assert inserted_row["settore"] == "Meccanica"
    assert inserted_row["note"] == "test"
    assert inserted_row["nome_azienda"] == "Unitec Srl"


def test_update_company_updates_fields():
    client = MagicMock()
    client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [
        {"id": 1, "stato": "contattata"}
    ]
    result = db.update_company(client, 1, stato="contattata")
    assert result["stato"] == "contattata"
    client.table.return_value.update.assert_called_once_with({"stato": "contattata"})
    client.table.return_value.update.return_value.eq.assert_called_once_with("id", 1)


def test_update_company_rejects_invalid_stato():
    client = MagicMock()
    with pytest.raises(ValueError, match="stato non valido"):
        db.update_company(client, 1, stato="non_esiste")


def test_get_stats_counts_by_stato_and_sums_valore():
    client = MagicMock()
    client.table.return_value.select.return_value.execute.return_value.data = [
        {"stato": "da_contattare", "valore": None},
        {"stato": "sponsor_confermato", "valore": "500"},
        {"stato": "sponsor_confermato", "valore": "300"},
        {"stato": "persa", "valore": None},
    ]
    stats = db.get_stats(client)
    assert stats["totale"] == 4
    assert stats["per_stato"]["sponsor_confermato"] == 2
    assert stats["per_stato"]["da_contattare"] == 1
    assert stats["valore_totale"] == 800.0
