from typing import List, Optional, Dict
from filtered_repo_factory import create_filtered_repo
from Client import Client, ClientShort, MyEntityRep, RepoObserver, FilteredSortedFile
import views
import re


def validate_client_fields(values: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    errors: dict[str, str] = {}
    cleaned = dict(values)

    for field, fn in [
        ("name", Client.valid_client_name),
        ("type_of_property", Client.valid_type_of_property),
        ("address", Client.valid_address),
        ("phone", Client.valid_phone),
    ]:
        try:
            cleaned[field] = fn(values.get(field, ""))
        except ValueError as e:
            errors[field] = str(e)

    return errors, cleaned


class ClientController(RepoObserver):
    def __init__(self, repo: MyEntityRep):
        self.repo = repo
        self.repo.attach(self)
        self._last_clients: Optional[List[Client]] = None
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type
        if event_type == "read_all":
            self._last_clients = data

    def get_index_page(
        self,
        type_of_property: str | None = None,
        name_q: str | None = None,
        phone_q: str | None = None,
        sort_by: str | None = None,
        order: str | None = None,
        storage: str = "db",
    ) -> str:

        type_of_property = (type_of_property or "").strip()
        name_q = (name_q or "").strip()
        phone_q = (phone_q or "").strip()
        sort_by = (sort_by or "").strip()
        order = (order or "asc").strip().lower()

        use_filter_or_sort = any([
            type_of_property,
            name_q,
            phone_q,
            sort_by,
        ])

        if use_filter_or_sort:
            filtered_repo = create_filtered_repo(self.repo)
            clients = filtered_repo.get_list(
                type_of_property=type_of_property,
                name_q=name_q,
                phone_q=phone_q,
                sort_by=sort_by,
                order=order,
            )
        else:
            self._last_clients = None
            self.repo.read_all()
            clients = self._last_clients or []

        shorts = [ClientShort(c) for c in clients]

        return views.render_client_list(
            shorts,
            filters={
                "type_of_property": type_of_property,
                "name_q": name_q,
                "phone_q": phone_q,
                "sort_by": sort_by,
                "order": order,
            },
            storage=storage,
        )

    def get_client_details_page(self, client_id: int, storage: str = "db") -> str:
        client = self.repo.get_by_id(client_id)
        return views.render_client_details(client, storage=storage)


class AddClientController(RepoObserver):
    def __init__(self, repo: MyEntityRep):
        self.repo = repo
        self.repo.attach(self)
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type

    def get_form_page(self, storage: str = "db") -> str:
        return views.render_client_form(
            title="Добавление клиента",
            action_url=f"/client/new?storage={storage}",
            submit_text="Сохранить",
            values={"name": "", "type_of_property": "", "address": "", "phone": ""},
        )

    def handle_submit(
        self,
        name: str,
        type_of_property: str,
        address: str,
        phone: str,
        storage: str = "db",
    ) -> str:
        raw_values = {
            "name": name,
            "type_of_property": type_of_property,
            "address": address,
            "phone": phone,
        }

        errors, cleaned = validate_client_fields(raw_values)
        if errors:
            return views.render_client_form(
                title="Добавление клиента",
                action_url=f"/client/new?storage={storage}",
                submit_text="Сохранить",
                errors=errors,
                values=raw_values,
            )

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

        return views.render_client_saved(
            title="Клиент добавлен",
            message=f'Клиент <b>{client.name}</b> добавлен с ID <b>{client.client_id}</b>.',
        )


class EditClientController(RepoObserver):
    def __init__(self, repo: MyEntityRep):
        self.repo = repo
        self.repo.attach(self)
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type

    def get_form_page(self, client_id: int, storage: str = "db") -> str:
        client = self.repo.get_by_id(client_id)
        if client is None:
            return views.render_layout("Ошибка", "<h1>Клиент не найден</h1>")

        values = {
            "name": client.name,
            "type_of_property": client.type_of_property,
            "address": client.address,
            "phone": client.phone,
        }
        return views.render_client_form(
            title="Редактирование клиента",
            action_url=f"/client/{client_id}/edit?storage={storage}",
            submit_text="Сохранить",
            values=values,
            client_id=client_id,
        )

    def handle_submit(
        self,
        client_id: int,
        name: str,
        type_of_property: str,
        address: str,
        phone: str,
        storage: str = "db",
    ) -> str:
        raw_values = {
            "name": name,
            "type_of_property": type_of_property,
            "address": address,
            "phone": phone,
        }

        errors, cleaned = validate_client_fields(raw_values)
        if errors:
            return views.render_client_form(
                title="Редактирование клиента",
                action_url=f"/client/{client_id}/edit?storage={storage}",
                submit_text="Сохранить",
                errors=errors,
                values=raw_values,
                client_id=client_id,
            )

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

        return views.render_client_saved(
            title="Изменения сохранены",
            message=f"Клиент #{client_id} обновлён.",
        )


class DeleteClientController(RepoObserver):
    def __init__(self, repo: MyEntityRep):
        self.repo = repo
        self.repo.attach(self)
        self._last_event: Optional[str] = None

    def update(self, event_type: str, data):
        self._last_event = event_type

    def get_confirm_page(self, client_id: int, storage: str = "db") -> str:
        client = self.repo.get_by_id(client_id)
        return views.render_delete_confirm(client, storage=storage)

    def handle_delete(self, client_id: int, storage: str = "db") -> str:
        try:
            self.repo.delete_client(client_id)
        except ValueError as e:
            return views.render_layout(
                "Ошибка удаления",
                f"<h1>Ошибка</h1><p>{e}</p><p><a href='javascript:window.close()'>Закрыть</a></p>",
            )
        return views.render_delete_success(client_id)
