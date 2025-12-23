from __future__ import annotations
from datetime import date, datetime


from datetime import date, datetime


class BaseInvestment:
    def __init__(
        self,
        client_id: int,
        security_id: int,
        amount,
        start_date,
        end_date=None,
        result=None,
    ):
        self.client_id = client_id
        self.security_id = security_id
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.result = result

    @property
    def client_id(self) -> int:
        return self._client_id

    @client_id.setter
    def client_id(self, value: int):
        self._client_id = self._valid_fk(value, "ClientID")

    @property
    def security_id(self) -> int:
        return self._security_id

    @security_id.setter
    def security_id(self, value: int):
        self._security_id = self._valid_fk(value, "SecurityID")

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value):
        try:
            v = float(value)
        except Exception:
            raise ValueError("Сумма инвестиции должна быть числом")
        if v <= 0:
            raise ValueError("Сумма инвестиции должна быть > 0")
        self._amount = v

    @property
    def start_date(self) -> date:
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = self._valid_date(value, required=True)

    @property
    def end_date(self) -> date | None:
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = self._valid_date(value, required=False)

    @property
    def result(self) -> float | None:
        return self._result

    @result.setter
    def result(self, value):
        if value is None or value == "":
            self._result = None
            return
        try:
            self._result = float(value)
        except Exception:
            raise ValueError("Результат должен быть числом")

    @staticmethod
    def _valid_fk(value, name: str) -> int:
        if not isinstance(value, int):
            raise ValueError(f"{name} должен быть int")
        if value < 0:
            raise ValueError(f"{name} должен быть >= 0")
        return value

    @staticmethod
    def _valid_date(value, required: bool):
        if value in (None, ""):
            if required:
                raise ValueError("Дата обязательна")
            return None

        if isinstance(value, date):
            return value

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseInvestment):
            return NotImplemented
        return (
            self.client_id == other.client_id
            and self.security_id == other.security_id
            and self.amount == other.amount
            and self.start_date == other.start_date
            and self.end_date == other.end_date
            and self.result == other.result
        )


class Investment(BaseInvestment):
    def __init__(
        self,
        data,
        client_id=None,
        security_id=None,
        amount=None,
        start_date=None,
        end_date=None,
        result=None,
    ):
        if isinstance(data, int):
            super().__init__(
                client_id,
                security_id,
                amount,
                start_date,
                end_date,
                result,
            )
            self.investment_id = data

        elif isinstance(data, dict):
            self.__init__(
                int(data["investment_id"]),
                int(data["client_id"]),
                int(data["security_id"]),
                data["amount"],
                data["start_date"],
                data.get("end_date"),
                data.get("result"),
            )

        elif isinstance(data, str):
            parts = data.split(";")
            self.__init__(
                int(parts[0]),
                int(parts[1]),
                int(parts[2]),
                parts[3],
                parts[4],
                parts[5] if parts[5] != "" else None,
                parts[6] if len(parts) > 6 else None,
            )

        else:
            raise TypeError(f"Неподдерживаемый тип данных: {type(data)}")

    @property
    def investment_id(self) -> int:
        return self._investment_id

    @investment_id.setter
    def investment_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("InvestmentID должен быть int")
        if value < 0:
            raise ValueError("InvestmentID должен быть >= 0")
        self._investment_id = value

    def __repr__(self) -> str:
        return (
            f"{self.investment_id} | "
            f"client={self.client_id} | "
            f"security={self.security_id} | "
            f"amount={self.amount} | "
            f"{self.start_date} → {self.end_date} | "
            f"result={self.result}"
        )


class InvestmentShort(BaseInvestment):
    def __init__(self, inv: Investment):
        self.investment_id = inv.investment_id
        super().__init__(
            inv.client_id,
            inv.security_id,
            inv.amount,
            inv.start_date,
            inv.end_date,
            inv.result,
        )

    def __str__(self):
        return (
            f"{self.investment_id} | "
            f"{self.client_id} → {self.security_id} | "
            f"{self.amount}"
        )
