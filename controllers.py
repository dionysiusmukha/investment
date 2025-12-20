from typing import List, Optional, Dict

from Client import Client, ClientShort, MyEntity_rep_DB, RepoObserver
import views
import re


class ClientController(RepoObserver):
    def __init__(self, repo: MyEntity_rep_DB):
        self.repo = repo
        self.repo.attach(self)

        self._last_clients: Optional[List[Client]] = None
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type
        if event_type == "read_all":
            self._last_clients = data

    def get_index_page(self) -> str:
        self._last_clients = None
        self.repo.read_all()
        clients = self._last_clients or []
        shorts = [ClientShort(c) for c in clients]
        return views.render_client_list(shorts)

    def get_client_details_page(self, client_id: int) -> str:
        client = self.repo.get_by_id(client_id)
        return views.render_client_details(client)


class AddClientController(RepoObserver):
    def __init__(self, repo: MyEntity_rep_DB):
        self.repo = repo
        self.repo.attach(self)
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type

    def get_from_page(self) -> str:
        return views.render_add_client_form()

    def handle_submit(
        self,
        name: str,
        type_of_property: str,
        address: str,
        phone: str,
    ) -> str:
        raw_values = {
            "name": name,
            "type_of_property": type_of_property,
            "address": address,
            "phone": phone,
        }

        errors, cleaned = self._validate(raw_values)
        if errors:
            return views.render_add_client_form(errors=errors, values=raw_values)

        client = Client(
            0,
            name=cleaned["name"],
            type_of_property=cleaned["type_of_property"],
            address=cleaned["address"],
            phone=cleaned["phone"],
        )

        try:
            self.repo.add_client(client)
        except ValueError as e:

            return views.render_add_client_form(
                errors={"_form": str(e)},
                values=raw_values
            )

        return views.render_add_client_success(client)

    def _validate(self, values: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
        errors: dict[str, str] = {}
        cleaned = dict(values)

        try:
            cleaned["name"] = Client.valid_client_name(values.get("name", ""))
        except ValueError as e:
            errors["name"] = str(e)

        try:
            cleaned["type_of_property"] = Client.valid_type_of_property(values.get("type_of_property", ""))
        except ValueError as e:
            errors["type_of_property"] = str(e)

        try:
            cleaned["phone"] = Client.valid_phone(values.get("phone", ""))
        except ValueError as e:
            errors["phone"] = str(e)

        try:
            cleaned["address"] = Client.valid_address(values.get("address", ""))
        except ValueError as e:
            errors["address"] = str(e)

        return errors, cleaned


class EditClientController(RepoObserver):
    def __init__(self, repo: MyEntity_rep_DB):
        self.repo = repo
        self.repo.attach(self)
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type

    def get_form_page(self, client_id: int) -> str:
        client = self.repo.get_by_id(client_id)
        if client is None:
            return views.render_layout(
                "Ошибка",
                f"<h1>Клиент не найден</h1><p><a href='javascript:window.close()'>Закрыть</a></p>",
            )

        values = {
            "name": client.name,
            "type_of_property": client.type_of_property,
            "address": client.address,
            "phone": client.phone,
        }
        return views.render_edit_client_form(client_id=client_id, values=values)

    def handle_submit(
        self,
        client_id: int,
        name: str,
        type_of_property: str,
        address: str,
        phone: str,
    ) -> str:
        raw_values = {
            "name": name,
            "type_of_property": type_of_property,
            "address": address,
            "phone": phone,
        }

        errors, cleaned = self._validate(raw_values)
        if errors:
            return views.render_edit_client_form(client_id=client_id, errors=errors, values=raw_values)

        new_client = Client(
            client_id,
            name=cleaned["name"],
            type_of_property=cleaned["type_of_property"],
            address=cleaned["address"],
            phone=cleaned["phone"],
        )

        try:
            self.repo.replace_client(client_id, new_client)
        except ValueError as e:
            return views.render_edit_client_form(
                client_id=client_id,
                errors={"_form": str(e)},
                values=raw_values,
            )

        return views.render_edit_client_success(new_client)

    def _validate(self, values: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
        errors: dict[str, str] = {}
        cleaned = dict(values)

        try:
            cleaned["name"] = Client.valid_client_name(values.get("name", ""))
        except ValueError as e:
            errors["name"] = str(e)

        try:
            cleaned["type_of_property"] = Client.valid_type_of_property(values.get("type_of_property", ""))
        except ValueError as e:
            errors["type_of_property"] = str(e)

        try:
            cleaned["phone"] = Client.valid_phone(values.get("phone", ""))
        except ValueError as e:
            errors["phone"] = str(e)

        try:
            cleaned["address"] = Client.valid_address(values.get("address", ""))
        except ValueError as e:
            errors["address"] = str(e)

        return errors, cleaned
