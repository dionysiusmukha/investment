from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from controllers import (
    ClientController,
    AddClientController,
    EditClientController,
    DeleteClientController,
)
from repo_factory import create_repo

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def make_controllers(storage: str):
    repo = create_repo(storage)
    return (
        ClientController(repo),
        AddClientController(repo),
        EditClientController(repo),
        DeleteClientController(repo),
    )


@app.get("/", response_class=HTMLResponse)
def index(
    storage: str = Query(default="db"),
    type_of_property: str | None = None,
    name_q: str | None = None,
    phone_q: str | None = None,
    sort_by: str | None = None,
    order: str | None = None,
):
    list_controller, _, _, _ = make_controllers(storage)
    return list_controller.get_index_page(
        type_of_property=type_of_property,
        name_q=name_q,
        phone_q=phone_q,
        sort_by=sort_by,
        order=order,
        storage=storage,
    )


@app.get("/client/new", response_class=HTMLResponse)
def new_client_form(storage: str = Query(default="db")):
    _, add_controller, _, _ = make_controllers(storage)
    return add_controller.get_form_page(storage=storage)


@app.post("/client/new", response_class=HTMLResponse)
def new_client_submit(
    storage: str = Query(default="db"),
    name: str = Form(...),
    type_of_property: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
):
    _, add_controller, _, _ = make_controllers(storage)
    return add_controller.handle_submit(
        name=name,
        type_of_property=type_of_property,
        address=address,
        phone=phone,
        storage=storage,
    )


@app.get("/client/{client_id}/edit", response_class=HTMLResponse)
def edit_client_form(client_id: int, storage: str = Query(default="db")):
    _, _, edit_controller, _ = make_controllers(storage)
    return edit_controller.get_form_page(client_id, storage=storage)


@app.post("/client/{client_id}/edit", response_class=HTMLResponse)
def edit_client_submit(
    client_id: int,
    storage: str = Query(default="db"),
    name: str = Form(...),
    type_of_property: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
):
    _, _, edit_controller, _ = make_controllers(storage)
    return edit_controller.handle_submit(
        client_id=client_id,
        name=name,
        type_of_property=type_of_property,
        address=address,
        phone=phone,
        storage=storage,
    )


@app.get("/client/{client_id}/delete", response_class=HTMLResponse)
def delete_confirm(client_id: int, storage: str = Query(default="db")):
    _, _, _, delete_controller = make_controllers(storage)
    return delete_controller.get_confirm_page(client_id, storage=storage)


@app.post("/client/{client_id}/delete", response_class=HTMLResponse)
def delete_submit(client_id: int, storage: str = Query(default="db")):
    _, _, _, delete_controller = make_controllers(storage)
    return delete_controller.handle_delete(client_id, storage=storage)


@app.get("/client/{client_id}", response_class=HTMLResponse)
def client_details(client_id: int, storage: str = Query(default="db")):
    list_controller, _, _, _ = make_controllers(storage)
    return list_controller.get_client_details_page(client_id, storage=storage)
