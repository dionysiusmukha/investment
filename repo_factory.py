from __future__ import annotations
import os
from Client import DatabaseManager, MyEntity_rep_DB, MyEntity_rep_json, MyEntity_rep_yaml
from dotenv import load_dotenv

from SecurityRepoDB import Security_rep_DB
from InvestmentRepoDB import Investment_rep_DB

from SecurityRepoFile import Security_rep_json, Security_rep_yaml
from InvestmentRepoFile import Investment_rep_json, Investment_rep_yaml


load_dotenv()

CLIENT_JSON = "static/resources/clients.json"
CLIENT_YAML = "static/resources/clients.yaml"

SECURITY_JSON = "static/resources/securities.json"
SECURITY_YAML = "static/resources/securities.yaml"

INVESTMENT_JSON = "static/resources/investments.json"
INVESTMENT_YAML = "static/resources/investments.yaml"


def _make_db() -> DatabaseManager:
    dsn = os.getenv("DB_DSN")
    if not dsn:
        raise RuntimeError("DB_DSN is not set")
    return DatabaseManager(dsn=dsn)


def create_client_repo(storage: str):
    storage = (storage or "db").lower()

    if storage == "db":
        db = _make_db()
        return MyEntity_rep_DB(db, table="public.clients")

    if storage == "json":
        return MyEntity_rep_json(CLIENT_JSON)

    if storage == "yaml":
        return MyEntity_rep_yaml(CLIENT_YAML)

    raise ValueError(f"Unknown storage: {storage}")


def create_security_repo(storage: str):
    storage = (storage or "db").lower()

    if storage == "db":
        db = _make_db()
        return Security_rep_DB(db, table="public.securities")
    if storage == "json":
        return Security_rep_json(SECURITY_JSON)

    if storage == "yaml":
        return Security_rep_yaml(SECURITY_YAML)

    raise ValueError(f"Unknown storage: {storage}")


def create_investment_repo(storage: str):
    storage = (storage or "db").lower()

    if storage == "db":
        db = _make_db()
        return Investment_rep_DB(db, table="public.investments")

    if storage == "json":
        return Investment_rep_json(INVESTMENT_JSON)

    if storage == "yaml":
        return Investment_rep_yaml(INVESTMENT_YAML)

    raise ValueError(f"Unknown storage: {storage}")


def create_repo(storage: str):
    return create_client_repo(storage)
