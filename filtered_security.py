from __future__ import annotations
from typing import Optional, Callable, Any, List

from Security import Security, SecurityShort

class FilteredSortedSecurityDB:
    def __init__(
        self,
        base_repo,
        filter_func: Optional[Callable[[Security], bool]] = None,
        sort_key: Optional[Callable[[Security], Any]] = None,
        reverse: bool = False,
    ):
        self._base_repo = base_repo
        self.filter_func = filter_func
        self.sort_key = sort_key
        self.reverse = reverse


    def read_all(self) -> List[Security]:
        return self._base_repo.read_all()

    def get_by_id(self, security_id: int) -> Security | None:
        return self._base_repo.get_by_id(security_id)

    def add_security(self, sec: Security) -> None:
        return self._base_repo.add_security(sec)

    def replace_security(self, security_id: int, new_sec: Security) -> None:
        return self._base_repo.replace_security(security_id, new_sec)

    def delete_security(self, security_id: int) -> None:
        return self._base_repo.delete_security(security_id)

    def _get_filtered_sorted(self) -> List[Security]:
        items = self._base_repo.read_all()

        if self.filter_func is not None:
            items = [s for s in items if self.filter_func(s)]

        if self.sort_key is not None:
            items.sort(key=self.sort_key, reverse=self.reverse)

        return items

    def get_filtered_sorted_list(self) -> List[Security]:
        return self._get_filtered_sorted()

    def get_list(
        self,
        name_q: str = "",
        security_type_q: str = "",
        income_min: str = "",
        income_max: str = "",
        sort_by: str = "",
        order: str = "asc",
    ) -> List[Security]:
        name_q = (name_q or "").strip().lower()
        security_type_q = (security_type_q or "").strip().lower()
        sort_by = (sort_by or "").strip().lower()
        order = (order or "asc").strip().lower()
        reverse = order == "desc"

        income_min_v = None
        income_max_v = None
        try:
            if income_min.strip() != "":
                income_min_v = float(income_min)
        except ValueError:
            income_min_v = None
        try:
            if income_max.strip() != "":
                income_max_v = float(income_max)
        except ValueError:
            income_max_v = None

        def filter_func(s: Security) -> bool:
            if name_q and name_q not in s.name.lower():
                return False
            if security_type_q and security_type_q not in s.security_type.lower():
                return False
            if income_min_v is not None and s.income < income_min_v:
                return False
            if income_max_v is not None and s.income > income_max_v:
                return False
            return True

        sort_key = None
        if sort_by in ("id", "security_id"):
            def sort_key(s: Security): return s.security_id
        elif sort_by == "name":
            def sort_key(s: Security): return s.name.lower()
        elif sort_by in ("security_type", "type"):
            def sort_key(s: Security): return s.security_type.lower()
        elif sort_by == "income":
            def sort_key(s: Security): return s.income

        self.filter_func = filter_func if (name_q or security_type_q or income_min_v is not None or income_max_v is not None) else None
        self.sort_key = sort_key
        self.reverse = reverse

        return self.get_filtered_sorted_list()


class FilteredSortedSecurityFile(FilteredSortedSecurityDB):
    pass
