import re
import json
import yaml
import psycopg2
from psycopg2.extras import RealDictCursor
from abc import ABC, abstractmethod
from typing import List, Callable, Any, Optional


class BaseClient:
    def __init__(self, name, type_of_property, phone):
        self.name = name
        self.type_of_property = type_of_property
        self.phone = phone

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = BaseClient.valid_client_name(value)

    @property
    def type_of_property(self):
        return self._type_of_property

    @type_of_property.setter
    def type_of_property(self, value):
        self._type_of_property = BaseClient.valid_type_of_property(value)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = BaseClient.valid_phone(value)

    @staticmethod
    def valid_client_name(name):
        name = name.strip()
        array_fio = name.split(' ')
        if name == '':
            raise ValueError("Строка ФИО должна быть непустой")
        if len(array_fio) not in [2, 3]:
            raise ValueError("ФИО должно быть разделено пробелами")
        for fio in array_fio:
            if not fio[0].isupper():
                raise ValueError(
                    "Каждая часть ФИО должна начинаться с заглавной буквы")
            if not re.fullmatch(r"[А-ЯЁ][а-яё]*(?:-[А-ЯЁ][а-яё]*)?\.?", fio):
                raise ValueError(
                    "ФИО должно состоять только из букв, дефисов и точек")

        return name

    @staticmethod
    def valid_type_of_property(type_of_property):
        acceptable_values = ["ООО", "ЗАО", "ОАО", "ИП"]
        if type_of_property == '':
            raise ValueError("Строка формы организации должна быть не пустой")
        f = False
        for i in acceptable_values:
            if i in type_of_property:
                f = True
        if not f:
            raise ValueError(
                'Строка формы организации должна содержать: "ООО", "ЗАО", "ОАО", "ИП"')
        return type_of_property

    @staticmethod
    def valid_phone(phone):
        if phone == '':
            raise ValueError("Строка номера телефона должна быть не пустой")

        if len(phone) > 12:
            raise ValueError("Телефон должен содержать не больше 12 знаков")
        pattern = re.compile(r'[+]?[7|8]?\d{10,11}')
        if not re.match(pattern, phone):
            raise ValueError("Неправильный формат телефона")

        if phone[0] == '+':
            phone = phone[1:]

        if phone[0] == '8' and len(phone) == 11:
            phone = '7' + phone[1:]

        if len(phone) == 10:
            phone = '7' + phone

        return phone

    def __str__(self):
        return f"{self.name} - {self.type_of_property}"

    def __repr__(self):
        return f"Name - {self.name}, Type of property -  {self.type_of_property}, Phone number - {self.phone})"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return (self.name == other.name and
                self.type_of_property == other.type_of_property
                and self.phone == other.phone)


class Client(BaseClient):
    def __init__(self, data, name=None, type_of_property=None, address=None, phone=None):
        if isinstance(data, int):
            super().__init__(name, type_of_property, phone)
            self.client_id = data
            self.address = address
        elif isinstance(data, dict):
            self.__init__(data['client_id'], data['name'],
                          data['type_of_property'], data['address'], data['phone'])
        elif isinstance(data, str):
            str_split = data.split(';')
            self.__init__(int(str_split[0]), str_split[1],
                          str_split[2], str_split[3], str_split[4])

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = Client.valid_client_id(value)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = Client.valid_address(value)

    @staticmethod
    def valid_client_id(client_id):
        if not isinstance(client_id, int):
            raise ValueError("ID клиента должно быть целым числом")
        if client_id < 0:
            raise ValueError("ID клиента должен быть >= 0")
        return client_id

    @staticmethod
    def valid_address(address):
        if address == '':
            raise ValueError("Строка адресса должна быть не пустой")
        return address

    def __repr__(self):
        return f"Client(ID - {self.client_id}, Name - {self.name}, Type of property -  {self.type_of_property}, Address - {self.address}, Phone number - {self.phone})"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return (self.client_id == other.client_id and self.name == other.name and
                self.type_of_property == other.type_of_property and self.address == other.address
                and self.phone == other.phone)


class ClientShort(BaseClient):
    def __init__(self, client):
        self.short_name = self.make_short_name(client.name)
        super().__init__(self.short_name, client.type_of_property, client.phone)

    def make_short_name(self, name):
        short_name = name.strip().split()
        if len(short_name) == 2:
            return f'{short_name[0]} {short_name[1][0]}'
        if len(short_name) == 3:
            return f'{short_name[0]} {short_name[1][0]}. {short_name[2][0]}.'
        return short_name

    def __str__(self):
        return f"{self.short_name} - {self.type_of_property} - {self.phone}"


class MyEntityRep(ABC):
    def __init__(self, filename: str):
        self.filename = filename
        self.clients: List[Client] = []
        self.read_all()

    @abstractmethod
    def read_all(self) -> List[Client]:
        pass

    @abstractmethod
    def write_all(self, file_to_write: str = None) -> None:
        pass

    def get_by_id(self, client_id: int) -> Client | None:
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort] | None:
        if k <= 0 or n <= 0:
            return None
        start = k * (n - 1)
        end = k * n
        selected_clients = self.clients[start:end]
        return [ClientShort(client) for client in selected_clients]

    def sort_by_name(self, reverse: bool = False) -> None:
        self.clients.sort(key=lambda client: client.name, reverse=reverse)

    def add_client(self, client: Client) -> None:
        if not self.clients:
            new_id = 1
        else:
            new_id = max(c.client_id for c in self.clients) + 1
        client.client_id = new_id
        self.clients.append(client)

    def replace_client(self, client_id: int, new_client: Client) -> None:
        for i, c in enumerate(self.clients):
            if c.client_id == client_id:
                new_client.client_id = c.client_id
                self.clients[i] = new_client
                return
        raise ValueError(f"Клиент с ID {client_id} не найден")

    def delete_client(self, client_id: int) -> None:
        for i, c in enumerate(self.clients):
            if c.client_id == client_id:
                self.clients.remove(c)
                return
        raise ValueError(f"Клиент с ID {client_id} не найден")

    def get_count(self) -> int:
        return len(self.clients)


class MyEntity_rep_json(MyEntityRep):
    def read_all(self) -> List[Client]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл {self.filename} не найден") from e
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Файл {self.filename} не является корректным JSON") from e

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список объектов (list)")

        clients: List[Client] = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"Некорректный элемент в {self.filename}")
            clients.append(Client(item))

        self.clients = clients
        return self.clients

    def write_all(self, file_to_write: str = None) -> None:
        data_to_write = [
            {
                "client_id": client.client_id,
                "name": client.name,
                "type_of_property": client.type_of_property,
                "address": client.address,
                "phone": client.phone
            } for client in self.clients
        ]
        filename = file_to_write if file_to_write else self.filename
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=4)


class MyEntity_rep_yaml(MyEntityRep):
    def read_all(self) -> List[Client]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл {self.filename} не найден") from e
        except yaml.YAMLError as e:
            raise ValueError(
                f"Файл {self.filename} не является корректным YAML-файлом") from e

        if data is None:
            self.clients = []
            return self.clients

        if not isinstance(data, list):
            raise ValueError(
                f"Некорректный формат YAML в {self.filename}. Ожидается list")

        clients: List[Client] = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"Неккоректный элемент в {self.filename}")

            clients.append(Client(item))

        self.clients = clients
        return self.clients

    def write_all(self, file_to_write: str = None) -> None:
        data_to_write = [
            {
                'client_id': client.client_id,
                'name': client.name,
                'type_of_property': client.type_of_property,
                'address': client.address,
                'phone': client.phone
            } for client in self.clients
        ]
        filename = file_to_write if file_to_write else self.filename
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data_to_write, f,
                           default_flow_style=False, allow_unicode=True)


class MyEntity_rep_DB(MyEntityRep):
    def __init__(self, db: "DatabaseManager", table: str = "public.clients"):
        self.db = db
        self.table = table
        self.clients = []

    def read_all(self) -> List[Client]:
        rows = self.db.fetch_all(
            f"SELECT client_id, name, type_of_property, address, phone FROM {self.table} ORDER BY client_id"
        )
        return [Client(dict(r)) for r in rows]

    def write_all(self, file_to_write: str = None) -> None:
        self.db.execute(f"TRUNCATE TABLE {self.table} RESTART IDENTITY")
        for c in self.clients:
            self.db.execute(
                f"INSERT INTO {self.table} (name, type_of_property, address, phone) VALUES (%s, %s, %s, %s)",
                (c.name, c.type_of_property, c.address, c.phone)
            )

    def get_by_id(self, client_id: int) -> Client | None:
        if client_id <= 0:
            return None
        row = self.db.fetch_one(
            f"SELECT client_id, name, type_of_property, address, phone FROM {self.table} WHERE client_id = %s",
            (client_id,)
        )
        return Client(dict(row)) if row else None

    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort] | None:
        if k <= 0 or n <= 0:
            return None
        offset = k * (n - 1)
        rows = self.db.fetch_all(
            f"SELECT client_id, name, type_of_property, address, phone FROM {self.table} ORDER BY client_id LIMIT %s OFFSET %s",
            (k, offset)
        )
        return [ClientShort(Client(dict(r))) for r in rows]

    def add_client(self, client: Client) -> None:
        row = self.db.execute_returning_one(
            f"INSERT INTO {self.table} (name, type_of_property, address, phone) VALUES (%s, %s, %s, %s) RETURNING client_id",
            (client.name, client.type_of_property, client.address, client.phone)
        )
        client.client_id = row["client_id"]

    def replace_client(self, client_id: int, new_client: Client) -> None:
        rc = self.db.execute(
            f"UPDATE {self.table} SET name=%s, type_of_property=%s, address=%s, phone=%s WHERE client_id=%s",
            (new_client.name, new_client.type_of_property,
             new_client.address, new_client.phone, client_id)
        )
        if rc == 0:
            raise ValueError(f"Клиент с ID {client_id} не найден")

    def delete_client(self, client_id: int) -> None:
        rc = self.db.execute(
            f"DELETE FROM {self.table} WHERE client_id=%s", (client_id,))
        if rc == 0:
            raise ValueError(f"Клиент с ID {client_id} не найден")

    def get_count(self) -> int:
        row = self.db.fetch_one(f"SELECT COUNT(*) AS cnt FROM {self.table}")
        return int(row["cnt"])


class DatabaseManager:
    _instance: "DatabaseManager | None" = None

    def __new__(cls, *args, **kwargs) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dsn: str,
                 cursor_factory=RealDictCursor,
                 autocommit: bool = True) -> None:
        if getattr(self, "_initialized", False):
            return
        self.dsn: str = dsn
        self.cursor_factory = cursor_factory
        self.autocommit: bool = autocommit
        self._conn = None
        self._initialized: bool = True
        self._ensure_connection()

    def _ensure_connection(self) -> None:
        if self._conn is None or self._conn.closed != 0:
            self._conn = psycopg2.connect(self.dsn)
            self._conn.autocommit = self.autocommit

    def fetch_all(self,
                  sql: str,
                  params: tuple | list | dict | None = None) -> list[dict]:
        self._ensure_connection()
        with self._conn.cursor(cursor_factory=self.cursor_factory) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return rows if rows is not None else []

    def fetch_one(self,
                  sql: str,
                  params: tuple | list | dict | None = None) -> dict | None:
        self._ensure_connection()
        with self._conn.cursor(cursor_factory=self.cursor_factory) as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def execute(self,
                sql: str, params: tuple | list | dict | None = None) -> int:
        self._ensure_connection()
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount

    def execute_returning_one(self,
                              sql: str, params: tuple | list | dict | None = None) -> dict | None:
        self._ensure_connection()
        with self._conn.cursor(cursor_factory=self.cursor_factory) as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def close(self) -> None:
        if self._conn and self._conn.closed == 0:
            self._conn.close()


class FilteredSortedDB(MyEntityRep):
    def __init__(
        self,
        base_repo: MyEntityRep,
        filter_func: Optional[Callable[[Client], bool]] = None,
        sort_key: Optional[Callable[[Client], Any]] = None,
        reverse: bool = False,
    ):
        self._base_repo = base_repo
        self.filter_func = filter_func
        self.sort_key = sort_key
        self.reverse = reverse
        self.filename = getattr(base_repo, "filename", "")
        self.clients: List[Client] = []

    def read_all(self) -> List[Client]:
        return self._base_repo.read_all()

    def write_all(self, file_to_write: str = None) -> None:
        return self._base_repo.write_all(file_to_write)

    def add_client(self, client: Client) -> None:
        return self._base_repo.add_client(client)

    def replace_client(self, client_id: int, new_client: Client) -> None:
        return self._base_repo.replace_client(client_id, new_client)

    def delete_client(self, client_id: int) -> None:
        return self._base_repo.delete_client(client_id)

    def get_by_id(self, client_id: int) -> Client | None:
        return self._base_repo.get_by_id(client_id)

    def sort_by_name(self, reverse: bool = False) -> None:
        if hasattr(self._base_repo, "sort_by_name"):
            return self._base_repo.sort_by_name(reverse)

    def _get_filtered_sorted_clients(self) -> List[Client]:
        clients = self._base_repo.read_all()

        if self.filter_func is not None:
            clients = [c for c in clients if self.filter_func(c)]

        if self.sort_key is not None:
            clients.sort(key=self.sort_key, reverse=self.reverse)

        return clients

    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort] | None:

        if k <= 0 or n <= 0:
            return None

        clients = self._get_filtered_sorted_clients()

        start = k * (n-1)
        end = k * n
        page = clients[start:end]

        return [ClientShort(c) for c in page]

    def get_count(self) -> int:
        if self.filter_func is None and self.sort_key is None:
            return self._base_repo.get_count()

        clients = self._get_filtered_sorted_clients()
        return len(clients)


class FilteredSortedFile(MyEntityRep):
    def __init__(
        self,
        base_repo: MyEntityRep,
        filter_func: Optional[Callable[[Client], bool]] = None,
        sort_key: Optional[Callable[[Client], Any]] = None,
        reverse: bool = False
    ):
        self._base_repo = base_repo
        self.filter_func = filter_func
        self.sort_key = sort_key
        self.reverse = reverse

        self.filename = getattr(base_repo, "filename", "")
        self.clients: List[Client] = base_repo.clients

    def read_all(self) -> List[Client]:
        clients = self._base_repo.read_all()
        self.clients = self._base_repo.clients
        return clients

    def write_all(self, file_to_write: str = None) -> None:
        return self._base_repo.write_all(file_to_write)

    def add_client(self, client: Client) -> None:
        self._base_repo.add_client(client)
        self.clients = self._base_repo.clients

    def replace_client(self, client_id: int, new_client: Client) -> None:
        self._base_repo.replace_client(client_id, new_client)
        self.clients = self._base_repo.clients

    def delete_client(self, client_id: int) -> None:
        self._base_repo.delete_client(client_id)
        self.clients = self._base_repo.clients

    def get_by_id(self, client_id: int) -> Client | None:
        return self._base_repo.get_by_id(client_id)

    def sort_by_name(self, reverse: bool = False) -> None:
        if hasattr(self._base_repo, "sort_by_name"):
            self._base_repo.sort_by_name(reverse)
            self.clients = self._base_repo.clients

    def _get_filtered_sorted_clients(self) -> List[Client]:
        clients = self._base_repo.read_all()

        if self.filter_func is not None:
            clients = [c for c in clients if self.filter_func(c)]

        if self.sort_key is not None:
            clients.sort(key=self.sort_key, reverse=self.reverse)

        return clients

    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort] | None:
        if k <= 0 or n <= 0:
            return None

        clients = self._get_filtered_sorted_clients()
        start = k * (n - 1)
        end = k * n
        page = clients[start:end]

        return [ClientShort(c) for c in page]

    def get_count(self) -> int:
        clients = self._get_filtered_sorted_clients()
        return len(clients)


try:
    db = DatabaseManager(
        "dbname=investment_db user=postgres password=den host=127.0.0.1 port=5432")
    base_repo = MyEntity_rep_DB(db)

    def krasnodar_filter(c: Client) -> bool:
        return "Краснодар" in c.address

    def name_key(c: Client):
        return c.name

    def only_ip(c: Client) -> bool:
        return "ИП" in c.type_of_property

    decorated_repo = FilteredSortedDB(
        base_repo,
        filter_func=krasnodar_filter,
        sort_key=name_key,
        reverse=False
    )

    print("Всего клиентов в БД:", base_repo.get_count())
    print("Клиентов из Краснодара:", decorated_repo.get_count())

    page = decorated_repo.get_k_n_short_list(k=5, n=1)
    for short in page:
        print(short)

    print("------------------------------------------")
    json_repo = MyEntity_rep_json("resources/clients.json")

    decorated_json = FilteredSortedFile(
        json_repo,
        filter_func=only_ip,
        sort_key=name_key,
        reverse=False
    )

    print("Всего клиентов в файле:", json_repo.get_count())
    print("Клиентов-ИП:", decorated_json.get_count())

    page = decorated_json.get_k_n_short_list(k=5, n=1)
    for short in page:
        print(short)

    print("------------------------------------------")

    yaml_repo = MyEntity_rep_yaml("resources/clients.yaml")

    decorated_json = FilteredSortedFile(
        yaml_repo,
        filter_func=only_ip,
        sort_key=name_key,
        reverse=False
    )

    print("Всего клиентов в файле:", yaml_repo.get_count())
    print("Клиентов-ИП:", decorated_json.get_count())

    page = decorated_json.get_k_n_short_list(k=5, n=1)
    for short in page:
        print(short)

except ValueError as e:
    print("Ошибка:", e)
except TypeError as e:
    print("Ошибка типа:", e)
