from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from Client import DatabaseManager, MyEntity_rep_DB
from controllers import ClientController

app = FastAPI()


def create_controller() -> ClientController:
    db = DatabaseManager(
        "dbname=investment_db user=postgres password=den host=127.0.0.1 port=5432"
    )

    repo = MyEntity_rep_DB(db)
    controller = ClientController(repo)
    return controller


controller = create_controller()


@app.get("/", response_class=HTMLResponse)
def index():
    return controller.get_index_page()


@app.get("/client/{client_id}", response_class=HTMLResponse)
def client_details(client_id: int):
    return controller.get_client_details_page(client_id)
