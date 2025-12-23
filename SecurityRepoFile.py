from __future__ import annotations
from typing import List
import json
import yaml

from Security import Security


class Security_rep_json:
    def __init__(self, filename: str):
        self.filename = filename
        self.securities: List[Security] = []

    def read_all(self) -> List[Security]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.securities = []
            return self.securities
        except json.JSONDecodeError as e:
            raise ValueError(f"Файл {self.filename} не является корректным JSON") from e

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список объектов (list)")

        self.securities = [Security(item) for item in data]
        return self.securities

    def write_all(self, file_to_write: str | None = None) -> None:
        filename = file_to_write or self.filename
        data_to_write = [
            {
                "security_id": s.security_id,
                "name": s.name,
                "security_type": s.security_type,
                "income": s.income,
            }
            for s in self.securities
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=4)

    def get_by_id(self, security_id: int) -> Security | None:
        self.read_all()
        for s in self.securities:
            if s.security_id == security_id:
                return s
        return None

    def add_security(self, sec: Security) -> None:
        self.read_all()
        new_id = max([s.security_id for s in self.securities], default=0) + 1
        sec.security_id = new_id
        self.securities.append(sec)
        self.write_all()

    def replace_security(self, security_id: int, new_sec: Security) -> None:
        self.read_all()
        for i, s in enumerate(self.securities):
            if s.security_id == security_id:
                new_sec.security_id = security_id
                self.securities[i] = new_sec
                self.write_all()
                return
        raise ValueError(f"Security с ID {security_id} не найден")

    def delete_security(self, security_id: int) -> None:
        self.read_all()
        before = len(self.securities)
        self.securities = [s for s in self.securities if s.security_id != security_id]
        if len(self.securities) == before:
            raise ValueError(f"Security с ID {security_id} не найден")
        self.write_all()


class Security_rep_yaml:
    def __init__(self, filename: str):
        self.filename = filename
        self.securities: List[Security] = []

    def read_all(self) -> List[Security]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            self.securities = []
            return self.securities
        except yaml.YAMLError as e:
            raise ValueError(f"Файл {self.filename} не является корректным YAML") from e

        if data is None:
            self.securities = []
            return self.securities

        if not isinstance(data, list):
            raise ValueError("YAML должен содержать список объектов (list)")

        self.securities = [Security(item) for item in data]
        return self.securities

    def write_all(self, file_to_write: str | None = None) -> None:
        filename = file_to_write or self.filename
        data_to_write = [
            {
                "security_id": s.security_id,
                "name": s.name,
                "security_type": s.security_type,
                "income": s.income,
            }
            for s in self.securities
        ]
        with open(filename, "w", encoding="utf-8") as f:
            yaml.safe_dump(data_to_write, f, default_flow_style=False, allow_unicode=True)

    def get_by_id(self, security_id: int) -> Security | None:
        self.read_all()
        for s in self.securities:
            if s.security_id == security_id:
                return s
        return None

    def add_security(self, sec: Security) -> None:
        self.read_all()
        new_id = max([s.security_id for s in self.securities], default=0) + 1
        sec.security_id = new_id
        self.securities.append(sec)
        self.write_all()

    def replace_security(self, security_id: int, new_sec: Security) -> None:
        self.read_all()
        for i, s in enumerate(self.securities):
            if s.security_id == security_id:
                new_sec.security_id = security_id
                self.securities[i] = new_sec
                self.write_all()
                return
        raise ValueError(f"Security с ID {security_id} не найден")

    def delete_security(self, security_id: int) -> None:
        self.read_all()
        before = len(self.securities)
        self.securities = [s for s in self.securities if s.security_id != security_id]
        if len(self.securities) == before:
            raise ValueError(f"Security с ID {security_id} не найден")
        self.write_all()
