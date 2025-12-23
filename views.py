from typing import Iterable, Mapping
from Client import Client, ClientShort
from urllib.parse import urlencode


def render_layout(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8" />
        <title>{title}</title>
        
         <script>
            function refreshOpener() {{
            if (window.opener && !window.opener.closed) {{
                try {{
                window.opener.location.reload();
                return true;
                }} catch (e) {{
                return false;
                }}
            }}
            return false;
            }}

            function closeAndRefresh() {{
            refreshOpener();
            window.close();
            }}

            // (крестик, Alt+F4) — попробуем обновить opener.
            window.addEventListener("beforeunload", function () {{
            refreshOpener();
            }});
        </script>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        {body}
    </body>
    </html>
    """


def render_client_list(
    clients: Iterable[ClientShort],
    filters: Mapping[str, str] | None = None,
    storage: str = "db",
) -> str:
    rows = []
    filters = filters or {}

    def build_url(base: str, params: dict[str, str]) -> str:
        qs = urlencode({k: v for k, v in params.items() if v is not None})
        return f"{base}?{qs}" if qs else base

    type_val = filters.get("type_of_property", "")
    name_q = filters.get("name_q", "")
    phone_q = filters.get("phone_q", "")
    sort_by = filters.get("sort_by", "")
    order = filters.get("order", "asc")

    form_action = build_url("/", {"storage": storage})

    filter_form = f"""
        <form method="get" action="/" style="margin-bottom:12px;">

        <input type="hidden" name="storage" value="{storage}">

        <label>Форма собственности:
            <select name="type_of_property">
            <option value="" {"selected" if type_val == "" else ""}>Все</option>
            <option value="ООО" {"selected" if type_val == "ООО" else ""}>ООО</option>
            <option value="ЗАО" {"selected" if type_val == "ЗАО" else ""}>ЗАО</option>
            <option value="ОАО" {"selected" if type_val == "ОАО" else ""}>ОАО</option>
            <option value="ИП"  {"selected" if type_val == "ИП" else ""}>ИП</option>
            </select>
        </label>

        <label style="margin-left:10px;">ФИО содержит:
            <input name="name_q" value="{name_q}">
        </label>

        <label style="margin-left:10px;">Телефон содержит:
            <input name="phone_q" value="{phone_q}">
        </label>

        <label style="margin-left:10px;">Сортировать по:
        <select name="sort_by">
            <option value="" {"selected" if sort_by == "" else ""}>Без сортировки</option>
            <option value="id" {"selected" if sort_by == "id" else ""}>ID</option>
            <option value="name" {"selected" if sort_by == "name" else ""}>ФИО</option>
            <option value="type" {"selected" if sort_by == "type" else ""}>Форма</option>
            <option value="phone" {"selected" if sort_by == "phone" else ""}>Телефон</option>
        </select>
        </label>

        <label style="margin-left:10px;">Порядок:
        <select name="order">
            <option value="asc" {"selected" if order == "asc" else ""}>↑</option>
            <option value="desc" {"selected" if order == "desc" else ""}>↓</option>
        </select>
        </label>

        <button type="submit" style="margin-left:10px;">Фильтровать</button>
        <a href="/?storage={storage}" style="margin-left:10px;">Сброс</a>

        </form>
        """

    for c in clients:
        details_url = build_url(f"/client/{c.client_id}", {"storage": storage})
        edit_url = build_url(f"/client/{c.client_id}/edit", {"storage": storage})
        delete_url = build_url(f"/client/{c.client_id}/delete", {"storage": storage})

        rows.append(
            f"<tr>"
            f"<td>{c.client_id}</td>"
            f"<td>{c.short_name}</td>"
            f"<td>{c.type_of_property}</td>"
            f"<td>{c.phone}</td>"
            f"<td>"
            f"<a href='#' onclick=\"window.open('{details_url}','_blank'); return false;\">Подробнее</a> | "
            f"<a href='#' onclick=\"window.open('{edit_url}','_blank'); return false;\">Редактировать</a> | "
            f"<a href='#' onclick=\"window.open('{delete_url}','_blank'); return false;\" style='color:#c00'>Удалить</a>"
            f"</td>"
        )

    new_url = build_url("/client/new", {"storage": storage})

    table = f"""
        <h1>Список клиентов</h1>

        <p>
            <a href="#" onclick="window.open('{new_url}','_blank'); return false;">Добавить клиента</a>
        </p>

        {filter_form}

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


def render_client_details(client: Client | None, storage: str = "db") -> str:
    if client is None:
        body = f"<h1>Клиент не найден</h1><p><a href='/?storage={storage}'>Назад</a></p>"
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


def render_client_form(
    title: str,
    action_url: str,
    submit_text: str,
    errors: dict[str, str] | None = None,
    values: dict[str, str] | None = None,
    client_id: int | None = None,
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

    header = f"<h1>{title}</h1>"
    if client_id is not None:
        header = f"<h1>{title} #{client_id}</h1>"

    body = f"""
    {header}
    {form_error_html}

    <form method="post" action="{action_url}">
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

    <button type="submit">{submit_text}</button>
    </form>

    <p><a href="javascript:closeAndRefresh()">Закрыть окно</a></p>
    """
    return render_layout(title, body)


def render_client_saved(title: str, message: str) -> str:
    body = f"""
    <h1>{title}</h1>
    <p>{message}</p>

    <script>
    if (window.opener && !window.opener.closed) {{
        try {{ window.opener.location.reload(); }} catch(e) {{}}
    }}
    </script>

    <p><a href="javascript:closeAndRefresh()">Закрыть окно</a></p>
    """
    return render_layout(title, body)


def render_delete_confirm(client: Client | None, storage: str = "db") -> str:
    if client is None:
        return render_layout(
            "Ошибка",
            "<h1>Клиент не найден</h1><p><a href='javascript:closeAndRefresh()'>Закрыть</a></p>",
        )

    body = f"""
    <h1>Удаление клиента #{client.client_id}</h1>

    <p>Вы точно хотите удалить клиента:</p>
    <ul>
    <li><b>ФИО:</b> {client.name}</li>
    <li><b>Форма:</b> {client.type_of_property}</li>
    <li><b>Адрес:</b> {client.address}</li>
    <li><b>Телефон:</b> {client.phone}</li>
    </ul>

    <form method="post" action="/client/{client.client_id}/delete?storage={storage}">
    <button type="submit" style="background:#c00;color:#fff;padding:6px 12px;border:0;cursor:pointer;">
        Удалить
    </button>
    <a href="javascript:window.close()" style="margin-left:12px">Отмена</a>
    </form>
    """
    return render_layout("Удаление клиента", body)


def render_delete_success(client_id: int) -> str:
    body = f"""
    <h1>Клиент удалён</h1>
    <p>Клиент #{client_id} удалён.</p>

    <script>
    if (window.opener && !window.opener.closed) {{
        try {{ window.opener.location.reload(); }} catch(e) {{}}
    }}
    </script>

    <p><a href="javascript:closeAndRefresh()">Закрыть окно</a></p>
    """
    return render_layout("Удалено", body)
