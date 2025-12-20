from typing import Iterable, Mapping
from Client import Client, ClientShort


def render_layout(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8" />
        <title>{title}</title>
        
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        {body}
    </body>
    </html>
    """


def render_client_list(clients: Iterable[ClientShort]) -> str:
    rows = []

    for c in clients:
        rows.append(
            f"<tr>"
            f"<td>{c.client_id}</td>"
            f"<td>{c.short_name}</td>"
            f"<td>{c.type_of_property}</td>"
            f"<td>{c.phone}</td>"
            f"<td>"
            f"<a href='/client/{c.client_id}' target='_blank'>Подробнее</a> | "
            f"<a href='/client/{c.client_id}/edit' target='_blank'>Редактировать</a>"
            f"</td>"
        )

    table = f"""
        <h1>Список клиентов</h1>

        <p>
            <a href="/client/new" target="_blank">Добавить клиента</a>
        </p>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Форма</th>
                    <th>Телефон</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {' '.join(rows)}
            </tbody>
    </table>
    """
    return render_layout("Клиенты", table)


def render_client_details(client: Client | None) -> str:
    if client is None:
        body = "<h1>Клиент не найден</h1><p><a href='/'>Назад</a></p>"
        return render_layout("Ошибка", body)

    body = f"""
    <h1>Клиент {client.client_id}</h1>
    <ul>
        <li><b>ФИО:</b> {client.name}</li>
        <li><b>Форма собственности:</b> {client.type_of_property}</li>
        <li><b>Адрес:</b> {client.address}</li>
        <li><b>Телефон:</b> {client.phone}</li>
    </ul>

    <button onclick="window.close()">Закрыть</button>
    """
    return render_layout(f"Клиент {client.client_id}", body)


def render_add_client_form(
        errors: Mapping[str, str] | None = None,
        values: Mapping[str, str] | None = None) -> str:

    errors = errors or {}
    values = values or {}

    def val(field: str) -> str:
        return values.get(field, "")

    def err(field: str) -> str:
        msg = errors.get(field)
        return f'<div style="color:red;fint-size:1rem">{msg}</div>' if msg else ""

    body = f"""
        <h1>Добавлениее клиента</h1>
            <form method="post" action="/client/new">
                <label>ФИО:<br>
                    <input type="text" name="name" value="{val('name')}" />
                    {err('name')}
                </label>
                <br><br>
                
                <label>Форма собственности:<br>
                    <input type="text" name="type_of_property" value="{val('type_of_property')}" />
                    {err('type_of_property')}
                </label>
                <br><br>

                <label>Адрес:<br>
                    <input type="text" name="address" value="{val('address')}" />
                    {err('address')}
                </label>
                <br><br>

                <label>Телефон:<br>
                    <input type="text" name="phone" value="{val('phone')}" />
                    {err('phone')}
                </label>
                <br><br>

                <button type="submit">Сохранить</button>
            </form>

            <p><a href="javascript:window.close()">Закрыть окно</a></p>
        """
    return render_layout("Новый клиент", body)


def render_add_client_success(client: Client) -> str:
    body = f"""
        <h1>Клиент добавлен</h1>
        <p>Клиент <b>{client.name}</b> успешно добавлен с ID <b>{client.client_id}</b>.</p>

        <p>Это окно можно закрыть.</p>
        <script>
            if (window.opener && !window.opener.closed) {{
                try {{
                    window.opener.location.reload();
                }} catch (e) {{}}
            }}
        </script>

        <p><a href="javascript:window.close()">Закрыть окно</a></p>
    """

    return render_layout("Клиент добавлен", body)


def render_edit_client_form(
    client_id: int,
    errors: dict[str, str] | None = None,
    values: dict[str, str] | None = None,
) -> str:
    errors = errors or {}
    values = values or {}

    def val(field: str) -> str:
        return values.get(field, "")

    def err(field: str) -> str:
        msg = errors.get(field)
        return f'<div style="color:red;font-size:0.9em">{msg}</div>' if msg else ""

    form_error = errors.get("_form")
    form_error_html = (
        f'<div style="color:red;margin-bottom:10px">{form_error}</div>' if form_error else ""
    )

    body = f"""
    <h1>Редактирование клиента #{client_id}</h1>
    {form_error_html}

    <form method="post" action="/client/{client_id}/edit">
    <label>ФИО:<br>
        <input type="text" name="name" value="{val('name')}" />
        {err('name')}
    </label>
    <br><br>

    <label>Форма собственности:<br>
        <input type="text" name="type_of_property" value="{val('type_of_property')}" />
        {err('type_of_property')}
    </label>
    <br><br>

    <label>Адрес:<br>
        <input type="text" name="address" value="{val('address')}" />
        {err('address')}
    </label>
    <br><br>

    <label>Телефон:<br>
        <input type="text" name="phone" value="{val('phone')}" />
        {err('phone')}
    </label>
    <br><br>

    <button type="submit">Сохранить</button>
    </form>

    <p><a href="javascript:window.close()">Закрыть окно</a></p>
    """
    return render_layout("Редактирование клиента", body)


def render_edit_client_success(client: Client) -> str:
    body = f"""
    <h1>Изменения сохранены</h1>
    <p>Клиент #{client.client_id} обновлён.</p>

    <script>
    if (window.opener && !window.opener.closed) {{
        try {{ window.opener.location.reload(); }} catch(e) {{}}
    }}
    </script>

    <p><a href="javascript:window.close()">Закрыть окно</a></p>
    """
    return render_layout("Клиент обновлён", body)
