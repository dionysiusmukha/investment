from __future__ import annotations
import re


class BaseSecurity:
    def __init__(self, name: str, security_type: str, income):
        self.name = name
        self.security_type = security_type
        self.income = income

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = BaseSecurity.valid_name(value)

    @property
    def security_type(self) -> str:
        return self._security_type

    @security_type.setter
    def security_type(self, value: str) -> None:
        self._security_type = BaseSecurity.valid_security_type(value)

    @property
    def income(self) -> float:
        return self._income

    @income.setter
    def income(self, value) -> None:
        self._income = BaseSecurity.valid_income(value)

    @staticmethod
    def valid_name(value: str) -> str:
        value = str(value).strip()
        if value == "":
            raise ValueError("Название ценной бумаги не может быть пустым")
        return value

    @staticmethod
    def valid_security_type(value: str) -> str:
        value = str(value).strip()
        if value == "":
            raise ValueError("Тип ценной бумаги не может быть пустым")
        return value

    @staticmethod
    def valid_income(value) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise ValueError("Доходность должна быть числом")
        return v

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseSecurity):
            return NotImplemented
        return (self.name, self.security_type, self.income) == (other.name, other.security_type, other.income)

    def __str__(self) -> str:
        return f"{self.name} ({self.security_type}) income={self.income}"


class Security(BaseSecurity):
    def __init__(self, data, name=None, security_type=None, income=None):
        if isinstance(data, int):
            super().__init__(name, security_type, income)
            self.security_id = data
        elif isinstance(data, dict):
            self.__init__(
                int(data["security_id"]),
                data["name"],
                data["security_type"],
                data["income"],
            )
        elif isinstance(data, str):
            parts = data.split(";")
            self.__init__(
                int(parts[0]),
                parts[1],
                parts[2],
                parts[3],
            )
        else:
            raise TypeError(f"Неподдерживаемый тип данных: {type(data)}")

    @property
    def security_id(self) -> int:
        return self._security_id

    @security_id.setter
    def security_id(self, value: int) -> None:
        self._security_id = Security.valid_security_id(value)

    @staticmethod
    def valid_security_id(value) -> int:
        if not isinstance(value, int):
            raise ValueError("SecurityID должен быть int")
        if value < 0:
            raise ValueError("SecurityID должен быть >= 0")
        return value

    def __repr__(self) -> str:
        return f"{self.security_id} - {self.name} - {self.security_type} - {self.income}"


class SecurityShort(BaseSecurity):

    def __init__(self, sec: Security):
        self.security_id = sec.security_id
        self.short_name = self.make_short_name(sec.name)
        super().__init__(self.short_name, sec.security_type, sec.income)

    def make_short_name(self, name: str) -> str:
        name = name.strip()
        if len(name) <= 18:
            return name
        return name[:18] + "…"

    def __str__(self) -> str:
        return f"{self.security_id} - {self.short_name} - {self.security_type} - {self.income}"
