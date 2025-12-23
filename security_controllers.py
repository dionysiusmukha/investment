from typing import Optional, List

import security_views as views
from Security import Security, SecurityShort
from filtered_security import FilteredSortedSecurityDB, FilteredSortedSecurityFile


def validate_security_fields(values: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    errors = {}
    cleaned = dict(values)

    try:
        cleaned["name"] = values.get("name", "").strip()
        if not cleaned["name"]:
            raise ValueError("Название не может быть пустым")
    except ValueError as e:
        errors["name"] = str(e)

    try:
        cleaned["security_type"] = values.get("security_type", "").strip()
        if not cleaned["security_type"]:
            raise ValueError("Тип не может быть пустым")
    except ValueError as e:
        errors["security_type"] = str(e)

    try:
        raw = values.get("income", "").strip()
        cleaned["income"] = str(float(raw)).rstrip("0").rstrip(".") if raw else ""
        if raw == "":
            raise ValueError("Доходность обязательна")
    except ValueError:
        errors["income"] = "Доходность должна быть числом"

    return errors, cleaned


class SecurityController:
    def __init__(self, repo):
        self.repo = repo

    def get_index_page(
        self,
        name_q: str | None = None,
        security_type_q: str | None = None,
        income_min: str | None = None,
        income_max: str | None = None,
        sort_by: str | None = None,
        order: str | None = None,
        storage: str = "db",
    ) -> str:
        name_q = (name_q or "").strip()
        security_type_q = (security_type_q or "").strip()
        income_min = (income_min or "").strip()
        income_max = (income_max or "").strip()
        sort_by = (sort_by or "").strip()
        order = (order or "asc").strip().lower()

        Decorator = FilteredSortedSecurityDB if storage == "db" else FilteredSortedSecurityFile
        decorated = Decorator(self.repo)

        securities = decorated.get_list(
            name_q=name_q,
            security_type_q=security_type_q,
            income_min=income_min,
            income_max=income_max,
            sort_by=sort_by,
            order=order,
        )

        shorts = [SecurityShort(s) for s in securities]
        return views.render_security_list(
            shorts,
            filters={
                "name_q": name_q,
                "security_type_q": security_type_q,
                "income_min": income_min,
                "income_max": income_max,
                "sort_by": sort_by,
                "order": order,
            },
            storage=storage,
        )


    def get_details_page(self, security_id: int, storage: str = "db") -> str:
        sec = self.repo.get_by_id(security_id)
        return views.render_security_details(sec, storage=storage)


class AddSecurityController:
    def __init__(self, repo):
        self.repo = repo

    def get_form_page(self, storage="db"):
        return views.render_security_form(
            title="Добавление бумаги",
            action_url=f"/security/new?storage={storage}",
            submit_text="Сохранить",
            values={"name": "", "security_type": "", "income": ""},
        )

    def handle_submit(self, name: str, security_type: str, income: str, storage="db"):
        raw = {"name": name, "security_type": security_type, "income": income}
        errors, cleaned = validate_security_fields(raw)
        if errors:
            return views.render_security_form(
                title="Добавление бумаги",
                action_url=f"/security/new?storage={storage}",
                submit_text="Сохранить",
                errors=errors,
                values=raw,
            )

        sec = Security(0, name=cleaned["name"], security_type=cleaned["security_type"], income=float(cleaned["income"]))
        self.repo.add_security(sec)
        return views.render_security_saved("Бумага добавлена", f"#{sec.security_id} добавлена.")


class EditSecurityController:
    def __init__(self, repo):
        self.repo = repo

    def get_form_page(self, security_id: int, storage: str = "db") -> str:
        sec = self.repo.get_by_id(security_id)
        if sec is None:
            return views.render_layout("Ошибка", "<h1>Бумага не найдена</h1>")

        values = {
            "name": sec.name,
            "security_type": sec.security_type,
            "income": str(sec.income),
        }

        return views.render_security_form(
            title="Редактирование бумаги",
            action_url=f"/security/{security_id}/edit?storage={storage}",
            submit_text="Сохранить",
            values=values,
            security_id=security_id,
        )

    def handle_submit(
        self,
        security_id: int,
        name: str,
        security_type: str,
        income: str,
        storage: str = "db",
    ) -> str:
        raw = {"name": name, "security_type": security_type, "income": income}
        errors, cleaned = validate_security_fields(raw)

        if errors:
            return views.render_security_form(
                title="Редактирование бумаги",
                action_url=f"/security/{security_id}/edit?storage={storage}",
                submit_text="Сохранить",
                errors=errors,
                values=raw,
                security_id=security_id,
            )

        new_sec = Security(
            security_id,
            name=cleaned["name"],
            security_type=cleaned["security_type"],
            income=float(cleaned["income"]),
        )

        try:
            self.repo.replace_security(security_id, new_sec)
        except ValueError as e:
            return views.render_security_form(
                title="Редактирование бумаги",
                action_url=f"/security/{security_id}/edit?storage={storage}",
                submit_text="Сохранить",
                errors={"_form": str(e)},
                values=raw,
                security_id=security_id,
            )

        return views.render_security_saved("Изменения сохранены", f"Бумага #{security_id} обновлена.")


class DeleteSecurityController:
    def __init__(self, repo):
        self.repo = repo

    def get_confirm_page(self, security_id: int, storage: str = "db") -> str:
        sec = self.repo.get_by_id(security_id)
        return views.render_security_delete_confirm(sec, storage=storage)

    def handle_delete(self, security_id: int, storage: str = "db") -> str:
        try:
            self.repo.delete_security(security_id)
        except ValueError as e:
            return views.render_layout(
                "Ошибка удаления",
                f"<h1>Ошибка</h1><p>{e}</p><p><a href='javascript:closeAndRefresh()'>Закрыть</a></p>",
            )
        return views.render_security_delete_success(security_id)
