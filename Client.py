import re


class Client:
    def __init__(self, client_id, name, type_of_property, address, phone):
        self.client_id = client_id
        self.name = name
        self.type_of_property = type_of_property
        self.address = address
        self.phone = phone

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
        if name == '':
            raise ValueError("Строка имени должна быть непустой")
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



try:
    c = Client(1,'    dede   ',"ООО zao","kalinina","89899993678")
    print(c.address)
except ValueError as e:
    print("Ошибка:", e)