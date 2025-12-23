from __future__ import annotations
from typing import List
import json
import yaml

from Investment import Investment


class Investment_rep_json:
    def __init__(self, filename: str):
        self.filename = filename
        self.investments: List[Investment] = []

    def read_all(self) -> List[Investment]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.investments = []
            return self.investments
        except json.JSONDecodeError as e:
            raise ValueError(f"Файл {self.filename} не является корректным JSON") from e

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список объектов (list)")

        self.investments = [Investment(item) for item in data]
        return self.investments

    def write_all(self, file_to_write: str | None = None) -> None:
        filename = file_to_write or self.filename
        data_to_write = [
            {
                "investment_id": inv.investment_id,
                "client_id": inv.client_id,
                "security_id": inv.security_id,
                "amount": inv.amount,
                "start_date": inv.start_date,
                "end_date": inv.end_date,
                "result": inv.result,
            }
            for inv in self.investments
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=4)

    def get_by_id(self, investment_id: int) -> Investment | None:
        self.read_all()
        for inv in self.investments:
            if inv.investment_id == investment_id:
                return inv
        return None

    def add_investment(self, inv: Investment) -> None:
        self.read_all()
        new_id = max([x.investment_id for x in self.investments], default=0) + 1
        inv.investment_id = new_id
        self.investments.append(inv)
        self.write_all()

    def replace_investment(self, investment_id: int, new_inv: Investment) -> None:
        self.read_all()
        for i, x in enumerate(self.investments):
            if x.investment_id == investment_id:
                new_inv.investment_id = investment_id
                self.investments[i] = new_inv
                self.write_all()
                return
        raise ValueError(f"Investment с ID {investment_id} не найден")

    def delete_investment(self, investment_id: int) -> None:
        self.read_all()
        before = len(self.investments)
        self.investments = [x for x in self.investments if x.investment_id != investment_id]
        if len(self.investments) == before:
            raise ValueError(f"Investment с ID {investment_id} не найден")
        self.write_all()


class Investment_rep_yaml:
    def __init__(self, filename: str):
        self.filename = filename
        self.investments: List[Investment] = []

    def read_all(self) -> List[Investment]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            self.investments = []
            return self.investments
        except yaml.YAMLError as e:
            raise ValueError(f"Файл {self.filename} не является корректным YAML") from e

        if data is None:
            self.investments = []
            return self.investments

        if not isinstance(data, list):
            raise ValueError("YAML должен содержать список объектов (list)")

        self.investments = [Investment(item) for item in data]
        return self.investments

    def write_all(self, file_to_write: str | None = None) -> None:
        filename = file_to_write or self.filename
        data_to_write = [
            {
                "investment_id": inv.investment_id,
                "client_id": inv.client_id,
                "security_id": inv.security_id,
                "amount": inv.amount,
                "start_date": inv.start_date,
                "end_date": inv.end_date,
                "result": inv.result,
            }
            for inv in self.investments
        ]
        with open(filename, "w", encoding="utf-8") as f:
            yaml.safe_dump(data_to_write, f, default_flow_style=False, allow_unicode=True)

    def get_by_id(self, investment_id: int) -> Investment | None:
        self.read_all()
        for inv in self.investments:
            if inv.investment_id == investment_id:
                return inv
        return None

    def add_investment(self, inv: Investment) -> None:
        self.read_all()
        new_id = max([x.investment_id for x in self.investments], default=0) + 1
        inv.investment_id = new_id
        self.investments.append(inv)
        self.write_all()

    def replace_investment(self, investment_id: int, new_inv: Investment) -> None:
        self.read_all()
        for i, x in enumerate(self.investments):
            if x.investment_id == investment_id:
                new_inv.investment_id = investment_id
                self.investments[i] = new_inv
                self.write_all()
                return
        raise ValueError(f"Investment с ID {investment_id} не найден")

    def delete_investment(self, investment_id: int) -> None:
        self.read_all()
        before = len(self.investments)
        self.investments = [x for x in self.investments if x.investment_id != investment_id]
        if len(self.investments) == before:
            raise ValueError(f"Investment с ID {investment_id} не найден")
        self.write_all()
