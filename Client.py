import re
import json
import yaml
from typing import List


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
        if len(array_fio) not in [2,3]:
            raise ValueError("ФИО должно быть разделено пробелами")
        for fio in array_fio:
            if not fio[0].isupper():
                raise ValueError("Каждая часть ФИО должна начинаться с заглавной буквы")
            if not re.fullmatch(r"[А-ЯЁ][а-яё]*(?:-[А-ЯЁ][а-яё]*)?\.?", fio):
                raise ValueError("ФИО должно состоять только из букв, дефисов и точек")

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
            raise ValueError('Строка формы организации должна содержать: "ООО", "ЗАО", "ОАО", "ИП"')
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
            self.__init__(data['client_id'], data['name'], data['type_of_property'], data['address'], data['phone'])
        elif isinstance(data, str):
            str_split = data.split(';')
            self.__init__(int(str_split[0]), str_split[1], str_split[2], str_split[3], str_split[4])



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

    def make_short_name(self,name):
        short_name = name.strip().split()
        if len(short_name) == 2:
            return f'{short_name[0]} {short_name[1][0]}'
        if len(short_name) == 3:
            return f'{short_name[0]} {short_name[1][0]}. {short_name[2][0]}.'
        return short_name
    def __str__(self):
        return f"{self.short_name} - {self.type_of_property} - {self.phone}"


class MyEntity_rep_json:
    def __init__(self, filename: str):
        self.filename = filename
        self.clients: List[Client] = []
        self.read_all()

    def read_all(self) -> List[Client]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.clients = []
            return self.clients

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список объектов (list)")

        loaded = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Каждый элемент JSON должен быть словарём (dict)")
            loaded.append(Client(item))
        self.clients = loaded
        return self.clients

    def write_all(self, file_to_write: str = None) -> None:
       data_to_write = []
       for client in self.clients:
           data_to_write.append(
               {
                   "client_id": client.client_id,
                   "name": client.name,
                   "type_of_property": client.type_of_property,
                   "address": client.address,
                   "phone": client.phone
               })
       filename = file_to_write if file_to_write else self.filename
       with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=4)

    def get_by_id(self, client_id: int) -> Client | None:
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def get_k_n_short_list(self, k: int, n: int) -> list[ClientShort] | None:
        if not(k > 0 and n > 0):
            return None
        start = k * (n-1)
        end = k * n
        selected_clients = self.clients[start:end]
        short_list = [ClientShort(client) for client in selected_clients]

        return short_list

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
        for c in self.clients:
            if c.client_id == client_id:
                del self.clients[client_id]
                return
        raise ValueError(f"Клиент с ID{client_id} не найден")

    def get_count(self) -> int:
        return len(self.clients)

class MyEntity_rep_yaml:
    def __init__(self, filename: str):
        self.filename = filename
        self.clients: List[Client] = []
        self.read_all()

    def read_all(self) -> List[Client]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError):
            print('Файл не удалось открыть')
            self.clients = []
            return self.clients

        if not data:
            self.clients = []
            return self.clients

        loaded = []
        for item in data:
            c = Client(item)
            loaded.append(c)
        self.clients = loaded
        return self.clients

    def write_all(self, file_to_write: str = None) -> None:
        data_to_write = []
        for client in self.clients:
            data_to_write.append({
                'client_id': client.client_id,
                'name': client.name,
                'type_of_property': client.type_of_property,
                'address': client.address,
                'phone': client.phone
            })

        filename = file_to_write if file_to_write else self.filename
        with open(self.filename, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data_to_write, f, default_flow_style=False, allow_unicode=True)

    def get_by_id(self, client_id: int) -> Client | None:
        for client in self.clients:
            if client_id == client.client_id:
                return client
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort] | None:
        if k <= 0 or n <= 0:
            return None

        start = k * (n-1)
        end = n * k
        list_of_clients = self.clients[start:end]
        res_list = [ClientShort(c) for c in list_of_clients]

        return res_list

    def sort_by_name(self, reverse=False) -> None:
        self.clients.sort(key=lambda client: client.name, reverse=reverse)

    def add_client(self, client: Client) -> None:
        if not self.clients:
            new_id = 1
        else:
            new_id = max(c.client_id for c in self.clients)
        client.client_id = new_id
        self.clients.append(client)
        return None

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






try:
    # with open('resources/clients.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    m = MyEntity_rep_yaml('./resources/clients.yaml')




except ValueError as e:
    print("Ошибка:", e)
except TypeError as e:
    print("Ошибка типа:", e)