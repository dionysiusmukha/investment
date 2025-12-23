from typing import List, Optional
from datetime import date, datetime

from Client import DatabaseManager
from Investment import Investment


def _to_iso(d) -> str:
    if isinstance(d, (date, datetime)):
        return d.date().isoformat() if isinstance(d, datetime) else d.isoformat()
    return str(d)


class Investment_rep_DB:
    def __init__(self, db: DatabaseManager, table: str = "public.investments"):
        self.db = db
        self.table = table

    def _row_to_investment(self, row: dict) -> Investment:
        return Investment(
            {
                "investment_id": int(row["investment_id"]),
                "client_id": int(row["client_id"]),
                "security_id": int(row["security_id"]),
                "amount": float(row["amount"]),
                "start_date": _to_iso(row["start_date"]),
                "end_date": _to_iso(row["end_date"]),
                "result": float(row.get("result", 0) or 0),
            }
        )

    def read_all(self) -> List[Investment]:
        rows = self.db.fetch_all(
            f"""
            SELECT investment_id, client_id, security_id, amount, start_date, end_date, result
            FROM {self.table}
            ORDER BY investment_id
            """
        )
        return [self._row_to_investment(r) for r in rows]

    def get_by_id(self, investment_id: int) -> Optional[Investment]:
        if investment_id <= 0:
            return None
        row = self.db.fetch_one(
            f"""
            SELECT investment_id, client_id, security_id, amount, start_date, end_date, result
            FROM {self.table}
            WHERE investment_id = %s
            """,
            (investment_id,),
        )
        return self._row_to_investment(row) if row else None

    def add_investment(self, inv: Investment) -> None:
        row = self.db.execute_returning_one(
            f"""
            INSERT INTO {self.table} (client_id, security_id, amount, start_date, end_date, result)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING investment_id
            """,
            (inv.client_id, inv.security_id, inv.amount, inv.start_date, inv.end_date, inv.result),
        )
        if not row:
            raise RuntimeError("INSERT не вернул investment_id")
        inv.investment_id = int(row["investment_id"])

    def replace_investment(self, investment_id: int, new_inv: Investment) -> None:
        rc = self.db.execute(
            f"""
            UPDATE {self.table}
            SET client_id=%s,
                security_id=%s,
                amount=%s,
                start_date=%s,
                end_date=%s,
                result=%s
            WHERE investment_id=%s
            """,
            (
                new_inv.client_id,
                new_inv.security_id,
                new_inv.amount,
                new_inv.start_date,
                new_inv.end_date,
                new_inv.result,
                investment_id,
            ),
        )
        if rc == 0:
            raise ValueError(f"Investment с ID {investment_id} не найден")

    def delete_investment(self, investment_id: int) -> None:
        rc = self.db.execute(
            f"DELETE FROM {self.table} WHERE investment_id=%s",
            (investment_id,),
        )
        if rc == 0:
            raise ValueError(f"Investment с ID {investment_id} не найден")

    def get_count(self) -> int:
        row = self.db.fetch_one(f"SELECT COUNT(*) AS cnt FROM {self.table}")
        return int(row["cnt"]) if row else 0
