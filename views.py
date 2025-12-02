from typing import Iterable
from Client import Client, ClientShort


def render_layout(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8" />
        <title>{title}</title>
        <style>
            body {{ font-family: sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 4px 8px; }}
            a {{ text-decoration: none; color: #0066cc; }}
        </style>
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
            f"<td><a href='/client/{c.client_id}'>Подробнее</a></td>"
            f"</tr>"
        )

    table = f"""
        <h1>Список клиентов</h1>
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
    <h1>Клиент #{client.client_id}</h1>
    <ul>
        <li><b>ФИО:</b> {client.name}</li>
        <li><b>Форма собственности:</b> {client.type_of_property}</li>
        <li><b>Адрес:</b> {client.address}</li>
        <li><b>Телефон:</b> {client.phone}</li>
    </ul>
    <p><a href="/">Назад к списку</a></p>
    """
    return render_layout(f"Клиент {client.client_id}", body)
