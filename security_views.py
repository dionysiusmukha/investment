from typing import Iterable, Mapping
from urllib.parse import urlencode

from Security import Security, SecurityShort


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


def _build_url(base: str, params: dict[str, str]) -> str:
    qs = urlencode({k: v for k, v in params.items() if v is not None})
    return f"{base}?{qs}" if qs else base


def render_security_list(
    securities: Iterable[SecurityShort],
    filters: Mapping[str, str] | None = None,
    storage: str = "db",
) -> str:
    filters = filters or {}
    rows: list[str] = []

    def build_url(base: str, params: dict[str, str]) -> str:
        qs = urlencode({k: v for k, v in params.items() if v is not None})
        return f"{base}?{qs}" if qs else base


    back_clients_url = build_url("/", {"storage": storage})
    new_url = build_url("/security/new", {"storage": storage})
    name_q = filters.get("name_q", "")
    security_type_q = filters.get("security_type_q", "")
    income_min = filters.get("income_min", "")
    income_max = filters.get("income_max", "")
    sort_by = filters.get("sort_by", "")
    order = filters.get("order", "asc")


    filter_form = f"""
        <p>
            <a href="{back_clients_url}">Клиенты</a>
        </p>

        <form method="get" action="/securities" style="margin-bottom:12px;">
            <input type="hidden" name="storage" value="{storage}">

            <label>Название содержит:
                <input name="name_q" value="{name_q}">
            </label>

            <label style="margin-left:10px;">Тип содержит:
                <input name="security_type_q" value="{security_type_q}">
            </label>

            <label style="margin-left:10px;">Доходность от:
                <input name="income_min" value="{income_min}" style="width:80px;">
            </label>

            <label style="margin-left:10px;">до:
                <input name="income_max" value="{income_max}" style="width:80px;">
            </label>

            <label style="margin-left:10px;">Сортировать по:
                <select name="sort_by">
                    <option value="" {"selected" if sort_by == "" else ""}>Без сортировки</option>
                    <option value="id" {"selected" if sort_by == "id" else ""}>ID</option>
                    <option value="name" {"selected" if sort_by == "name" else ""}>Название</option>
                    <option value="security_type" {"selected" if sort_by == "security_type" else ""}>Тип</option>
                    <option value="income" {"selected" if sort_by == "income" else ""}>Доходность</option>
                </select>
            </label>

            <label style="margin-left:10px;">Порядок:
                <select name="order">
                    <option value="asc" {"selected" if order == "asc" else ""}>↑</option>
                    <option value="desc" {"selected" if order == "desc" else ""}>↓</option>
                </select>
            </label>

            <button type="submit" style="margin-left:10px;">Применить</button>
            <a href="/securities?storage={storage}" style="margin-left:10px;">Сброс</a>
        </form>
    """

    for s in securities:
        details_url = build_url(f"/security/{s.security_id}", {"storage": storage})
        edit_url = build_url(f"/security/{s.security_id}/edit", {"storage": storage})
        delete_url = build_url(f"/security/{s.security_id}/delete", {"storage": storage})

        rows.append(
            f"<tr>"
            f"<td>{s.security_id}</td>"
            f"<td>{s.name}</td>"
            f"<td>{s.security_type}</td>"
            f"<td>{s.income}</td>"
            f"<td>"
            f"<a href='#' onclick=\"window.open('{details_url}','_blank'); return false;\">Подробнее</a> | "
            f"<a href='#' onclick=\"window.open('{edit_url}','_blank'); return false;\">Редактировать</a> | "
            f"<a href='#' onclick=\"window.open('{delete_url}','_blank'); return false;\" style='color:#c00'>Удалить</a>"
            f"</td>"
            f"</tr>"
        )

    table = f"""
        <h1>Ценные бумаги</h1>

        <p>
            <a href="#" onclick="window.open('{new_url}','_blank'); return false;">Добавить бумагу</a>
        </p>

        {filter_form}

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Название</th>
                    <th>Тип</th>
                    <th>Доходность</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {' '.join(rows) if rows else '<tr><td colspan="5">Пусто</td></tr>'}
            </tbody>
        </table>
    """
    return render_layout("Ценные бумаги", table)


def render_security_details(sec: Security | None, storage: str = "db") -> str:
    if sec is None:
        return render_layout("Ошибка", "<h1>Ценная бумага не найдена</h1>")

    body = f"""
    <h1>Ценная бумага #{sec.security_id}</h1>
    <ul>
      <li><b>Название:</b> {sec.name}</li>
      <li><b>Тип:</b> {sec.security_type}</li>
      <li><b>Доходность:</b> {sec.income}</li>
    </ul>

    <button onclick="window.close()">Закрыть</button>
    """
    return render_layout(f"Security {sec.security_id}", body)


def render_security_form(
    title: str,
    action_url: str,
    submit_text: str,
    errors: dict[str, str] | None = None,
    values: dict[str, str] | None = None,
    security_id: int | None = None,
) -> str:
    errors = errors or {}
    values = values or {}

    def val(k: str) -> str:
        return values.get(k, "")

    def err(k: str) -> str:
        msg = errors.get(k)
        return f"<div style='color:red;font-size:0.9em'>{msg}</div>" if msg else ""

    form_error = errors.get("_form")
    form_error_html = f"<div style='color:red;margin-bottom:10px'>{form_error}</div>" if form_error else ""

    header = f"<h1>{title}</h1>" if security_id is None else f"<h1>{title} #{security_id}</h1>"

    body = f"""
    {header}
    {form_error_html}

    <form method="post" action="{action_url}">
      <label>Название:<br>
        <input type="text" name="name" value="{val('name')}"/>
        {err('name')}
      </label><br><br>

      <label>Тип:<br>
        <input type="text" name="security_type" value="{val('security_type')}"/>
        {err('security_type')}
      </label><br><br>

      <label>Доходность:<br>
        <input type="text" name="income" value="{val('income')}"/>
        {err('income')}
      </label><br><br>

      <button type="submit">{submit_text}</button>
    </form>

    <p><a href="javascript:closeAndRefresh()">Закрыть окно</a></p>
    """
    return render_layout(title, body)


def render_security_delete_confirm(sec: Security | None, storage: str = "db") -> str:
    if sec is None:
        return render_layout("Ошибка", "<h1>Бумага не найдена</h1><p><a href='javascript:closeAndRefresh()'>Закрыть</a></p>")

    body = f"""
    <h1>Удаление бумаги #{sec.security_id}</h1>
    <p>Вы точно хотите удалить:</p>
    <ul>
      <li><b>Название:</b> {sec.name}</li>
      <li><b>Тип:</b> {sec.security_type}</li>
      <li><b>Доходность:</b> {sec.income}</li>
    </ul>

    <form method="post" action="/security/{sec.security_id}/delete?storage={storage}">
      <button type="submit" style="background:#c00;color:#fff;padding:6px 12px;border:0;cursor:pointer;">Удалить</button>
      <a href="javascript:window.close()" style="margin-left:12px">Отмена</a>
    </form>
    """
    return render_layout("Удаление бумаги", body)


def render_security_saved(title: str, message: str) -> str:
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


def render_security_delete_success(security_id: int) -> str:
    body = f"""
    <h1>Бумага удалена</h1>
    <p>Бумага #{security_id} удалена.</p>
    <p><a href="javascript:closeAndRefresh()">Закрыть окно</a></p>
    """
    return render_layout("Удалено", body)
