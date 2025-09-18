import re
import json


class Client:
    def __init__(self, data, name=None, type_of_property=None, address=None, phone=None):
        if isinstance(data, int):
            self.client_id = data
            self.name = name
            self.type_of_property = type_of_property
            self.address = address
            self.phone = phone
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
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = Client.valid_client_name(value)

    @property
    def type_of_property(self):
        return self._type_of_property
    @type_of_property.setter
    def type_of_property(self, value):
        self._type_of_property = Client.valid_type_of_property(value)

    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, value):
        self._address = Client.valid_address(value)

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self, value):
        self._phone = Client.valid_phone(value)



    @staticmethod
    def valid_client_id(client_id):
        if not isinstance(client_id, int):
            raise ValueError("ID клиента должно быть целым числом")
        if client_id < 0:
            raise ValueError("ID клиента должен быть >= 0")
        return client_id

    @staticmethod
    def valid_client_name(name):
        name = name.strip()
        array_fio = name.split(' ')
        if name == '':
            raise ValueError("Строка ФИО должна быть непустой")
        if len(array_fio) != 3:
            raise ValueError("ФИО должно быть разделено пробелами")
        for fio in array_fio:
            if fio != fio.capitalize():
                raise ValueError("Каждая  часть ФИО должна начинаться с заглавной буквы")

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
    def valid_address(address):
        if address == '':
            raise ValueError("Строка адресса должна быть не пустой")
        return address

    @staticmethod
    def valid_phone(phone):
        if phone == '':
            raise ValueError("Строка номера телефона должна быть не пустой")

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
        return f"Client(ID - {self.client_id}, Name - {self.name}, Type of property -  {self.type_of_property}, Address - {self.address}, Phone number - {self.phone})"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return (self.client_id == other.client_id and self.name == other.name and
                self.type_of_property == other.type_of_property and self.address == other.address
                and self.phone == other.phone)


try:
    with open('./resources/ex.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    c1 = Client(data)
    print(c1.client_id)
    print(c1.name)
    print(c1.type_of_property)
    print(c1.address)

    c2 = Client('0;Хрущёв Никита Сергеевич;ИП Кукурузка;с. Кузькина Мать;79993215566')
    print(c2.client_id)
    print(c2.name)
    print(c2.type_of_property)
    print(c2.address)

    print(c2)
    print(repr(c2))

    print(c1 == c2)
    c3 = c1
    print(c1 == c3)
except ValueError as e:
    print("Ошибка:", e)
except TypeError as e:
    print("Ошибка типа:", e)