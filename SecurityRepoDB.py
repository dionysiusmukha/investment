from typing import List, Optional

from Client import DatabaseManager
from Security import Security


class Security_rep_DB:
    def __init__(self, db: DatabaseManager, table: str = "public.securities"):
        self.db = db
        self.table = table

    def _row_to_security(self, row: dict) -> Security:
        return Security(
            {
                "security_id": int(row["security_id"]),
                "name": str(row["name"]),
                "security_type": str(row["security_type"]),
                "income": float(row["income"]),
            }
        )

    def read_all(self) -> List[Security]:
        rows = self.db.fetch_all(
            f"""
            SELECT security_id, name, security_type, income
            FROM {self.table}
            ORDER BY security_id
            """
        )
        return [self._row_to_security(r) for r in rows]

    def get_by_id(self, security_id: int) -> Optional[Security]:
        if security_id <= 0:
            return None
        row = self.db.fetch_one(
            f"""
            SELECT security_id, name, security_type, income
            FROM {self.table}
            WHERE security_id = %s
            """,
            (security_id,),
        )
        return self._row_to_security(row) if row else None

    def add_security(self, sec: Security) -> None:
        row = self.db.execute_returning_one(
            f"""
            INSERT INTO {self.table} (name, security_type, income)
            VALUES (%s, %s, %s)
            RETURNING security_id
            """,
            (sec.name, sec.security_type, sec.income),
        )
        if not row:
            raise RuntimeError("INSERT не вернул security_id")
        sec.security_id = int(row["security_id"])

    def replace_security(self, security_id: int, new_sec: Security) -> None:
        rc = self.db.execute(
            f"""
            UPDATE {self.table}
            SET name=%s,
                security_type=%s,
                income=%s
            WHERE security_id=%s
            """,
            (new_sec.name, new_sec.security_type, new_sec.income, security_id),
        )
        if rc == 0:
            raise ValueError(f"Security с ID {security_id} не найден")

    def delete_security(self, security_id: int) -> None:
        rc = self.db.execute(
            f"DELETE FROM {self.table} WHERE security_id=%s",
            (security_id,),
        )
        if rc == 0:
            raise ValueError(f"Security с ID {security_id} не найден")

    def get_count(self) -> int:
        row = self.db.fetch_one(f"SELECT COUNT(*) AS cnt FROM {self.table}")
        return int(row["cnt"]) if row else 0
