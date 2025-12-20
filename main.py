from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from Client import DatabaseManager, MyEntity_rep_DB
from controllers import ClientController, AddClientController, EditClientController, DeleteClientController

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def create_repos_and_controllers() -> ClientController:
    db = DatabaseManager(
        "dbname=investment_db user=postgres password=den host=127.0.0.1 port=5432"
    )

    repo = MyEntity_rep_DB(db)
    list_controller = ClientController(repo)
    add_controller = AddClientController(repo)
    edit_controller = EditClientController(repo)
    delete_controller = DeleteClientController(repo)
    return list_controller, add_controller, edit_controller, delete_controller


list_controller, add_controller, edit_controller, delete_controller = create_repos_and_controllers()


@app.get("/", response_class=HTMLResponse)
def index(
    type_of_property: str | None = Query(default=None),
    name_q: str | None = Query(default=None),
    phone_q: str | None = Query(default=None),
):
    return list_controller.get_index_page(
        type_of_property=type_of_property,
        name_q=name_q,
        phone_q=phone_q,
    )


@app.get("/client/new", response_class=HTMLResponse)
def new_client_form():
    return add_controller.get_from_page()


@app.post("/client/new", response_class=HTMLResponse)
def new_client_submit(
        name: str = Form(...),
        type_of_property: str = Form(...),
        address: str = Form(...),
        phone: str = Form(...),):

    return add_controller.handle_submit(
        name=name,
        type_of_property=type_of_property,
        address=address,
        phone=phone,
    )


@app.get("/client/{client_id}/edit", response_class=HTMLResponse)
def edit_client_form(client_id: int):
    return edit_controller.get_form_page(client_id)


@app.post("/client/{client_id}/edit", response_class=HTMLResponse)
def edit_client_submit(
    client_id: int,
    name: str = Form(...),
    type_of_property: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
):
    return edit_controller.handle_submit(
        client_id=client_id,
        name=name,
        type_of_property=type_of_property,
        address=address,
        phone=phone,
    )


@app.get("/client/{client_id}/delete", response_class=HTMLResponse)
def delete_confirm(client_id: int):
    return delete_controller.get_confirm_page(client_id)


@app.post("/client/{client_id}/delete", response_class=HTMLResponse)
def delete_submit(client_id: int):
    return delete_controller.handle_delete(client_id)


@app.get("/client/{client_id}", response_class=HTMLResponse)
def client_details(client_id: int):
    return list_controller.get_client_details_page(client_id)
