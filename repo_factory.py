from Client import (
    MyEntityRep,
    MyEntity_rep_DB,
    MyEntity_rep_json,
    MyEntity_rep_yaml,
    DatabaseManager,
)


def create_repo(storage: str) -> MyEntityRep:
    storage = (storage or "db").lower()

    if storage == "db":
        db = DatabaseManager(
            "dbname=investment_db user=postgres password=den host=127.0.0.1 port=5432"
        )
        return MyEntity_rep_DB(db)

    if storage == "json":
        return MyEntity_rep_json(filename="static/resources/clients.json")

    if storage == "yaml":
        return MyEntity_rep_yaml(filename="static/resources/clients.yaml")

    raise ValueError(f"Unknown storage: {storage}")
