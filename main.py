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
from repo_factory import create_security_repo
from security_controllers import (
    SecurityController, AddSecurityController, EditSecurityController, DeleteSecurityController
)
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


def make_security_controllers(storage: str):
    repo = create_security_repo(storage)
    return (
        SecurityController(repo),
        AddSecurityController(repo),
        EditSecurityController(repo),
        DeleteSecurityController(repo),
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

@app.get("/securities", response_class=HTMLResponse)
def securities_index(
    storage: str = Query(default="db"),
    name_q: str | None = None,
    security_type_q: str | None = None,
    income_min: str | None = None,
    income_max: str | None = None,
    sort_by: str | None = None,
    order: str | None = None,
):
    repo = create_security_repo(storage)
    controller = SecurityController(repo)
    return controller.get_index_page(
        name_q=name_q,
        security_type_q=security_type_q,
        income_min=income_min,
        income_max=income_max,
        sort_by=sort_by,
        order=order,
        storage=storage,
    )


@app.get("/security/new", response_class=HTMLResponse)
def security_new_form(storage: str = Query(default="db")):
    _, add_c, _, _ = make_security_controllers(storage)
    return add_c.get_form_page(storage=storage)


@app.post("/security/new", response_class=HTMLResponse)
def security_new_submit(
    storage: str = Query(default="db"),
    name: str = Form(...),
    security_type: str = Form(...),
    income: str = Form(...),
):
    _, add_c, _, _ = make_security_controllers(storage)
    return add_c.handle_submit(name=name, security_type=security_type, income=income, storage=storage)


@app.get("/security/{security_id}/edit", response_class=HTMLResponse)
def security_edit_form(security_id: int, storage: str = Query(default="db")):
    _, _, edit_c, _ = make_security_controllers(storage)
    return edit_c.get_form_page(security_id, storage=storage)


@app.post("/security/{security_id}/edit", response_class=HTMLResponse)
def security_edit_submit(
    security_id: int,
    storage: str = Query(default="db"),
    name: str = Form(...),
    security_type: str = Form(...),
    income: str = Form(...),
):
    _, _, edit_c, _ = make_security_controllers(storage)
    return edit_c.handle_submit(security_id, name, security_type, income, storage=storage)


@app.get("/security/{security_id}/delete", response_class=HTMLResponse)
def security_delete_confirm(security_id: int, storage: str = Query(default="db")):
    _, _, _, del_c = make_security_controllers(storage)
    return del_c.get_confirm_page(security_id, storage=storage)


@app.post("/security/{security_id}/delete", response_class=HTMLResponse)
def security_delete_submit(security_id: int, storage: str = Query(default="db")):
    _, _, _, del_c = make_security_controllers(storage)
    return del_c.handle_delete(security_id, storage=storage)


@app.get("/security/{security_id}", response_class=HTMLResponse)
def security_details(security_id: int, storage: str = Query(default="db")):
    list_c, _, _, _ = make_security_controllers(storage)
    return list_c.get_details_page(security_id, storage=storage)
