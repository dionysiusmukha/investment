from typing import List, Optional

from Client import Client, ClientShort, MyEntity_rep_DB, RepoObserver
import views


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
